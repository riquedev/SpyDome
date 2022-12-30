import {useTranslation} from 'react-i18next'

interface ITranslator {
    path: string;
    fn: (text: string) => string;
}

const Translator = ({path,fn}: ITranslator) => {
    const {t} = useTranslation()
    return (
        <>
            {fn ? fn(t(path)) : t(path)}
        </>
    )
}

export default Translator
