import Markdown from "marked-react"

export default function AIResponse({ message, vocab }) {
    return (
        <div className="card shadow rounded-4 mb-4 border-success">
            <div className="card-body">
                <Markdown className="card-text">{message}</Markdown>
                <img className="rounded-circle" style={{ height: '30px' }} src="ai_icon.jpg" alt="An green, flower-like image representing the AI" />
                {vocab.length > 0 && <p style={{marginTop: '10px'}}>Vocabulary: {vocab.map((word, i) => {
                    return <span key={i}>{word.word}{i === vocab.length - 1 ? '.' : ','} </span>
                })}</p>}
            </div>
        </div>
    )
}