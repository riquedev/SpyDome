import type {AppProps} from 'next/app'
import {Box, ChakraProvider, Flex, Spinner, Stack, useColorModeValue, Skeleton} from '@chakra-ui/react';
import {SessionProvider, useSession} from "next-auth/react"
import 'i18n';
import {PropsWithChildren} from "react";

export default function App({Component, pageProps: {session, ...pageProps}}: AppProps) {
    return (
        <ChakraProvider>
            <SessionProvider session={session}>
                {Component.auth ? (
                    <Auth {...Component.auth}>
                        <Component {...pageProps} />
                    </Auth>
                ) : (
                    <Component {...pageProps} />
                )}
            </SessionProvider>
        </ChakraProvider>
    )
}

// @ts-ignore
function Auth({role, loading, unauthorized, children}: PropsWithChildren) {
    // if `{ required: true }` is supplied, `status` can only be "loading" or "authenticated"
    const {status} = useSession({required: true})
    if (status == "loading") {
        return loading ? loading : (
            <Stack direction={['column', 'row']} spacing='0px'>
                <Flex
                    alignItems={'center'}
                    justifyContent={'center'}
                    textAlign={'center'}
                >
                    <Spinner
                        position={'absolute'}
                        thickness='3px'
                        speed='0.55s'
                        emptyColor='gray.200'
                        color='red.500'
                        size='xl'
                        margin={'auto 0'}
                        bottom={'0'}
                        top={'0'}
                    />

                <Skeleton>
                    <Box w='100vw' h='100vh' bg='yellow.200'/>
                </Skeleton>
                </Flex>
            </Stack>
        )
    }

    return children
}
