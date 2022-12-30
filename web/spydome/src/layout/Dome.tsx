import {
    Box,
    Heading,
    Input,
    InputGroup,
    InputLeftElement,
    Spacer,
    Stack,
    SimpleGrid,
    Flex,
    HStack,
    InputRightElement
} from "@chakra-ui/react";
import Translator from "../components/i18n/Translator";
import {capitalizeFirstLetter} from "../utils";
import {SearchIcon} from "@chakra-ui/icons";

export default function DomeLayout() {
    return (
        <Box p={4}>
            <Heading as='h2' size='xl'>
                <Translator path={'common.operations'} fn={capitalizeFirstLetter}/>
            </Heading>
            <Stack direction={['column', 'row']} pt={4} justifyContent={'space-between'} spacing={['18px', '40px']}>
                <InputGroup>
                    <Input type='text' placeholder='Phone number' maxW={'600px'}/>
                </InputGroup>
                <InputGroup>
                    <Spacer/>
                    <InputRightElement>
                        <SearchIcon color='gray.300'/>
                    </InputRightElement>
                    <Input type='tel' placeholder='Phone number' maxW={'600px'}/>
                </InputGroup>
            </Stack>
        </Box>
    )
}
