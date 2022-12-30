import NextAuth from "next-auth"
import CredentialsProvider from 'next-auth/providers/credentials';
import jwt_decode from "jwt-decode";


interface SpyDomeCredentials {
    username: string;
    password: string;
}

const refreshSpyDomeToken = async ({token, user, account}) => {
    try {
        if (user && user.data) {
            const {refresh} = user.data.token
            const {SPYDOME_URL, SPYDOME_API_VERSION} = process.env;
            const authUrl = `${SPYDOME_URL}/api/${SPYDOME_API_VERSION}`
            const res = await fetch(`${authUrl}/token/refresh/`, {
                method: 'POST',
                body: JSON.stringify({refresh}),
                headers: {
                    'Content-Type': 'application/json',
                    'Accept-Language': 'en-US',
                },
            });
            const response = await res.json();

            if (!response.ok) {
                throw response
            }
            const decodedData = jwt_decode(response.access)
            console.log("REFRESH=========", {
                ...token,
                accessToken: response.access,
                accessTokenExpires: new Date(decodedData.exp * 1000),
                refreshToken: response.refresh ?? refresh,
            })
            return {
                ...token,
                accessToken: response.access,
                accessTokenExpires: new Date(decodedData.exp * 1000),
                refreshToken: response.refresh ?? refresh,
            }
        }
        return {
            ...token,
            error: "RefreshAccessTokenError",
        }
    } catch (error) {
        console.log(error)

        return {
            ...token,
            error: "RefreshAccessTokenError",
        }
    }
}

export default NextAuth({
    providers: [
        CredentialsProvider({
            id: "spydome",
            type: "credentials",
            // The name to display on the sign in form (e.g. 'Sign in with...')
            name: 'Spyder Dome',
            // The credentials is used to generate a suitable form on the sign in page.
            // You can specify whatever fields you are expecting to be submitted.
            // e.g. domain, username, password, 2FA token, etc.
            // You can pass any HTML attribute to the <input> tag through the object.
            credentials: {
                username: {
                    label: 'username',
                    type: 'text',
                    placeholder: 'robert.swift',
                },
                password: {label: 'Password', type: 'password'},
            },
            async authorize(credentials: SpyDomeCredentials, req) {
                const payload = {
                    ...credentials
                };
                const {SPYDOME_URL, SPYDOME_API_VERSION} = process.env;
                const authUrl = `${SPYDOME_URL}/api/${SPYDOME_API_VERSION}`
                const res = await fetch(`${authUrl}/token/`, {
                    method: 'POST',
                    body: JSON.stringify(payload),
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept-Language': 'en-US',
                    },
                });

                const response = await res.json();

                if (!res.ok) {
                    throw new Error(response.detail);
                }
                // If no error and we have user data, return it
                if (res.ok && response) {
                    const {refresh, access} = response;
                    const data = jwt_decode(refresh)
                    const {first_name, last_name, id, email} = data
                    return {
                        data: {
                            first_name,
                            last_name,
                            id,
                            email,
                            token: {refresh, access}
                        }
                    }
                }

                // Return null if user data could not be retrieved
                return null;
            }
        }),
        // ...add more providers here
    ],
    secret: process.env.JWT_SECRET,
    pages: {
        signIn: '/login',
    },
    callbacks: {
        async jwt({token, user, account}) {
            if (account && user) {
                let data = {
                    ...token,
                    accessToken: user.data.token.access,
                    refreshToken: user.data.token.refresh,
                    user
                }
                const decodedData = jwt_decode(data.accessToken);
                data['accessTokenExpires'] = new Date(decodedData.exp * 1000)
                return data;
            }

            if (Date.now() < token.accessTokenExpires) {
                return token
            }


            return await refreshSpyDomeToken({token, user, account});
        },

        async session({session, token, user}) {
            session.user.accessToken = token.accessToken;
            session.user.refreshToken = token.refreshToken;
            session.user.accessTokenExpires = token.accessTokenExpires;
            session.user.first_name = token.user.data.first_name
            session.user.last_name = token.user.data.last_name
            session.user.name = `${session.user.first_name} ${session.user.last_name}`
            session.user.email = token.user.data.email
            session.user.id = token.user.data.id
            session.error = token.error;
            return session;
        },
    },
    theme: {
        colorScheme: 'auto', // "auto" | "dark" | "light"
        brandColor: '', // Hex color code #33FF5D
        logo: '/logo/SpyDome.png', // Absolute URL to image
    },
    // Enable debug messages in the console if you are having problems
    debug: process.env.NODE_ENV === 'development',
});
