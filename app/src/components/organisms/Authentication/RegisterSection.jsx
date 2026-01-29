import RegisterForm from '@/components/molecules/RegisterForm';

export default function RegisterSection({className="", onSubmit, message}) {
    return (
        <div className={`${className} bg-dark`}>
            <RegisterForm onSubmit={onSubmit} message={message}/>
        </div>
    );
}