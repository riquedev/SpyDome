import Head from 'next/head'
import Navbar from "../../components/Navbar";
import DomeLayout from "../../layout/Dome";


export default function Dome() {
    return (
        <>
            <Head>
                <title>Dashboard | SpyDome</title>
                <meta name="viewport" content="width=device-width, initial-scale=1"/>
                <link rel="icon" href="/favicon.ico"/>
            </Head>
            <Navbar/>
            <DomeLayout/>
        </>
    )
}

Dome.auth = {
    role: "admin",
    unauthorized: "/", // redirect to this url
}
