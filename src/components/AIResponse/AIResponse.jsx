import Markdown from "marked-react"

export default function AIResponse({message}) {
    return (
        <div className="card shadow rounded-4 mb-4 border-success">
            <div className="card-body">
            <Markdown className="card-text">{message}</Markdown>
            <img className="rounded-circle" style={{height: '30px'}} src="ai_icon.jpg" alt="An green, flower-like image representing the AI" />
            </div>
        </div>
    )
}