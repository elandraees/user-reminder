import React, { useState } from 'react';
import { createNewAccount, IAccount } from '../services/account-service';

const CreateAccount = (props:{setStepId:React.Dispatch<React.SetStateAction<number>>; setEmailAddress:React.Dispatch<React.SetStateAction<string>>;}) => {

    const [accountState, setAccountState] = useState<IAccount>({
        'email_address':'',
        'password':''
    })

    const [resultMessage, setResultMessage] = useState<string>('')
    const [hasError, setError] = useState<boolean>(false)
    const [errorFields, setErrorFields] = useState<[string]>()

    const handleChange = (prop: keyof IAccount) => (event: React.ChangeEvent<HTMLInputElement>) => {
        setAccountState({ ...accountState, [prop]: event.target.value });
    };

    const createAccount = () => {
        setError(false)
        setResultMessage("")
         createNewAccount(accountState).then(response => {

            if (response.success)
            {
                props.setEmailAddress(accountState.email_address)
                props.setStepId(2)
            }
                
         })
         .catch(err => {

            if (err.response && err.response.data)
            {
                var res : IAccount = err.response.data.result
                var message = ""
                var errorFields: [string] = ['']

                let key: keyof IAccount;
                for(key in res) {
                    message = message + res[key] + '\n'
                    errorFields.push(key)
                }

                setErrorFields(errorFields)
                setError(true)
                setResultMessage(message)
            }
            else
                alert(err)
            

        })
         
    }

    return (
    <div className="w-full">

            <h3 className="text-3xl font-bold tracki text-center mt-12 sm:text-5xl mb-10">Create Account</h3>

            <div className={'pb-5 ' + (resultMessage != '' ? 'w-1/2 m-auto' : 'w-0')}>
                <p className={'rounded pl-2 text-white whitespace-pre opacity-85 '+ (hasError ? 'bg-red-500' : 'bg-green-500')}>
                    {resultMessage}
                </p>
            </div>
            
            <div className='m-auto w-1/2'>
                <label className='block w-full mt-2 mb-2 font-bold text-2xl'>
                    Email Address
                </label>
                <input type="text"
                            className='block mb-2 p-2 box-border border-2 rounded-md w-full' 
                            id="email_address" 
                            name="email_address" 
                            onChange={handleChange('email_address')}
                            placeholder="Enter your email address"/>

                <label className='block w-full mt-10 mb-2 font-bold text-2xl'>
                    Password
                </label>
                <input type="password"
                            className='block mb-2 p-2 box-border border-2 rounded-md w-full'
                            id="password" 
                            name="password"
                            onChange={handleChange('password')}
                            placeholder="Enter your Password"/>

                <label className='block w-full mt-10 mb-2 font-bold text-2xl'>
                    Confirm Password
                </label>
                <input type="password"
                            className='block mb-2 p-2 box-border border-2 rounded-md w-full'
                            id="confirmPassword" 
                            name="confirmPassword"
                            placeholder="Enter your Password"/>
                            
                <div className="wrap text-center mt-10 mb-10">
                    <button type="button" onClick={createAccount} id="login" className='rounded-lg border-0 text-white w-full bg-emerald-500 text-lg cursor-pointer hover:bg-emerald-600 p-2'>
                            Submit
                    </button>
                </div>
            
                {/* <p className="text-center">Registered? 
                    <a href="#"
                        className="italic hover:underline">
                            Login to your account
                    </a>
                </p> */}
            </div>
            
      </div>
    )

}

export default CreateAccount