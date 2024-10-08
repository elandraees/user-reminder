import React, { useState, useEffect } from 'react';

const ProductDisplay = (props: {productId:string | undefined;  emailAddress: string}) => {

    useEffect(() => {
        // Submit the form automatically after the component is mounted
        
        const form = document.getElementById('checkout-form') as HTMLFormElement | null;
        form?.submit();
    }, []);

    return (
    <div>
        <form id="checkout-form" action="http://127.0.0.1:5001/stripe/create-checkout-session" method="POST">

            <input type="hidden" name="priceId" value={props.productId} />
            <input type="hidden" name="emailAddress" value={props.emailAddress} />
            <div>
                <h2 className="text-3xl font-bold tracki text-center mt-12 sm:text-5xl pt-40">Loading Checkout...</h2>
            </div>
        </form>
    </div>
    )
};

const SuccessDisplay = (props:{ sessionId:string|null }) => {
  useEffect(() => {
    // Submit the form automatically after the component is mounted
    const form = document.getElementById('manage-form') as HTMLFormElement | null;
    form?.submit();
}, []);
    return (
      <section>
        <form action="http://127.0.0.1:5001/stripe/create-portal-session" method="POST" id = 'manage-form'>
          <input
            type="hidden"
            id="session-id"
            name="session_id"
            value={props.sessionId ? props.sessionId : ''}
          />
          <div>
                <h2 className="text-3xl font-bold tracki text-center mt-12 sm:text-5xl pt-40">Redirecting to your account...</h2>
            </div>
        </form>
      </section>
    );
};

const Message = (props:{ message:string }) => (
    <section>
      <p>{props.message}</p>
    </section>
);

const Checkout = (props: {productId:string | undefined; emailAddress: string}) => {

    let [message, setMessage] = useState('');
    let [success, setSuccess] = useState(false);
    let [sessionId, setSessionId] = useState<string|null>('');

    useEffect(() => {
        // Check to see if this is a redirect back from Checkout
        const query = new URLSearchParams(window.location.search);
    
        if (query.get('success')) {
          setSuccess(true);
          setSessionId(query.get('session_id'));
        }
    
        if (query.get('canceled')) {
          setSuccess(false);
          setMessage(
            "Order canceled -- continue to shop around and checkout when you're ready."
          );
        }
    }, [sessionId]);

    if (!success && message === '') {
        return <ProductDisplay productId={props.productId} emailAddress={props.emailAddress} />;
      } else if (success && sessionId !== '') {
        return <SuccessDisplay sessionId={sessionId} />;
      } else {
        return <Message message={message} />;
      }
}
export default Checkout