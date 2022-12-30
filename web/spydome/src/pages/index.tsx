import {
    Flex,
    Box,
    FormControl,
    FormLabel,
    Input,
    InputGroup,
    HStack,
    InputRightElement,
    Stack,
    Button,
    Heading,
    Text,
    useColorModeValue,
} from '@chakra-ui/react';
import {useState} from 'react';
import Head from 'next/head'
import Image from 'next/image'
import {signIn, getSession} from "next-auth/react"

import {ViewIcon, ViewOffIcon} from '@chakra-ui/icons';
import Translator from "../components/i18n/Translator";
import {capitalizeFirstLetter} from "../utils";


export default function Home() {
    const [showPassword, setShowPassword] = useState(false);
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")

    return (
        <>
            <Head>
                <title>SpyDome</title>
                <meta name="viewport" content="width=device-width, initial-scale=1"/>
                <link rel="icon" href="/favicon.ico"/>
            </Head>
            <Flex
                minH={'100vh'}
                align={'center'}
                justify={'center'}
                bg={useColorModeValue('gray.50', 'gray.800')}>
                <Stack spacing={8} mx={'auto'} maxW={'lg'} py={12} px={6}>
                    <Stack align={'center'}>
                        <Image src={'/logo/SpyDome.png'} alt={'SpyDome'} width={100} height={100}/>
                        <Heading fontSize={'4xl'} textAlign={'center'}>
                            <Translator path={'common.login'} fn={capitalizeFirstLetter}/>
                        </Heading>
                        <Text fontSize={'lg'} color={'gray.600'}>
                            <Translator path={'phares.what_are_we_doing_today'} fn={(text) => `${text}?`}/>
                        </Text>
                    </Stack>
                    <Box
                        rounded={'lg'}
                        bg={useColorModeValue('white', 'gray.700')}
                        boxShadow={'lg'}
                        p={8}>
                        <Stack spacing={4}>

                            <FormControl id="username" isRequired>
                                <FormLabel>
                                    <Translator path={'common.username'} fn={capitalizeFirstLetter}/>
                                </FormLabel>
                                <Input type="text"
                                       minW={'100%'}
                                       value={username}
                                       onChange={(event) => setUsername(event.target.value)}/>
                            </FormControl>
                            <FormControl id="password" isRequired>
                                <FormLabel>
                                    <Translator path={'common.password'} fn={capitalizeFirstLetter}/>
                                </FormLabel>
                                <InputGroup>
                                    <Input
                                        type={showPassword ? 'text' : 'password'}
                                        value={password}
                                        onChange={(event) => setPassword(event.target.value)}
                                    />
                                    <InputRightElement h={'full'}>
                                        <Button
                                            variant={'ghost'}
                                            onClick={() =>
                                                setShowPassword((showPassword) => !showPassword)
                                            }>
                                            {showPassword ? <ViewIcon/> : <ViewOffIcon/>}
                                        </Button>
                                    </InputRightElement>
                                </InputGroup>
                            </FormControl>
                            <Stack spacing={10} pt={2}>
                                <Button
                                    loadingText="Submitting"
                                    size="lg"
                                    bg={'blue.400'}
                                    color={'white'}
                                    onClick={() => {
                                        signIn('spydome', {
                                            username: username,
                                            password: password
                                        })
                                    }
                                    }
                                    _hover={{
                                        bg: 'blue.500',
                                    }}>
                                    <Translator path={'common.submit'} fn={capitalizeFirstLetter}/>
                                </Button>
                            </Stack>
                        </Stack>
                    </Box>
                </Stack>
            </Flex>
        </>
    )
}

export async function getServerSideProps(context: any) {
    const session = await getSession(context)
    if (session) {
        return {
            redirect: {
                destination: '/dome',
                permanent: false,
            },
        }
    }

    return {
        props: {}
    }
}
