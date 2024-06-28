export default function UserResponse({message}) {
    return (
        <div className="card rounded-4 shadow mb-4">
            <div className="card-body">
            <p className="card-text text-end">{message}</p>
            </div>
        </div>
    )
}