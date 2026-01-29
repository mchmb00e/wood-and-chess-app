import LoginForm from '@/components/molecules/LoginForm';

export default function LoginSection({className="", onSubmit, message}) {
    return (
        <div className={`${className} bg-dark`}>
            <LoginForm onSubmit={onSubmit} message={message}/>
        </div>
    );
}