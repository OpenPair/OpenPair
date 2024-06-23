import Markdown from "marked-react"

export default function AIResponse({ message, vocab }) {
    // if (vocab.length > 0) {
    //     let edited_message = message.split(' ')
    //     // console.log(edited_message);
    //     // let index_of_words = []
    //     edited_message = edited_message.map((word) => {
    //         for (let v of vocab) {
    //             if (word && word.toLowerCase().startsWith(v.word.toLowerCase())) {
    //                 // index_of_words.push(i)
    //                 return (
    //                     <span key={v.id} style={{ color: 'red', display: 'inline' }}>{word} </span>
    //                 )
    //             }
    //             return word
    //         }
    //     })
    //     console.log(edited_message.join(' '));
    //     let blocked_message_array = []
    //     let str = ''
    //     edited_message.map((part, i) => {
    //         // console.log('Part: ', part);
    //         if (typeof part !== 'object') {
    //             str += `${part} `
    //             // console.log('STRING:', str);
    //         } else {
    //             blocked_message_array.push(str)
    //             str = ''
    //             blocked_message_array.push(part)
    //         }
    //         if (i === edited_message.length - 1) {
    //             blocked_message_array.push(str)
    //         }
    //     })
    //     console.log(blocked_message_array);
    //     // console.log(index_of_words);
    //     return (
    //         <div className="card shadow rounded-4 mb-4 border-success">
    //             <div className="card-body">
    //                 {blocked_message_array.map(chunk => {
    //                     if (typeof chunk !== 'object') {
    //                         return <Markdown>{chunk}</Markdown>
    //                         // return `${chunk} `
    //                     }
    //                     return chunk
    //                 })}
    //                 <img className="rounded-circle" style={{ height: '30px' }} src="ai_icon.jpg" alt="An green, flower-like image representing the AI" />
    //             </div>
    //         </div>)
    // }
    return (
        <div className="card shadow rounded-4 mb-4 border-success">
            <div className="card-body">
                <Markdown className="card-text">{message}</Markdown>
                <img className="rounded-circle" style={{ height: '30px' }} src="ai_icon.jpg" alt="An green, flower-like image representing the AI" />
                {vocab.length > 0 && <p>Vocabulary: {vocab.map((word, i) => {
                    return <span>{word.word}{i === vocab.length - 1 ? '.' : ','} </span>
                })}</p>}
            </div>
        </div>
    )
}