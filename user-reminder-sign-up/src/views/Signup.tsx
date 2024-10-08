
import React, { useState } from 'react';
import CreateAccount from '../components/CreateAccount';
import Checkout from '../components/Checkout';
import PricingView from '../components/PricingView';

const Signup = () => {

    const [productId, setProductId] = useState<string>("")
    const [stepId, setStepId] = useState<number>(0)
    const [emailAddress, setEmailAddress]  = useState<string>("")

    var view = <PricingView setProductId={setProductId} setStepId={setStepId}/>
    if (stepId == 1)
        view = <CreateAccount setStepId={setStepId} setEmailAddress={setEmailAddress}/>
    if (stepId == 2)
        view = <Checkout productId={productId} emailAddress={emailAddress}/>


    return (
        <div>
        {
            view
        }
        </div>
    )       
}

export default Signup