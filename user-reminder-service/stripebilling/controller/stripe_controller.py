import os
from flask import Flask, redirect, request
from flask import Blueprint
from flask import Flask, redirect, jsonify, json, request, current_app

import stripe

# This test secret API key is a placeholder. Don't include personal details in requests with this key.
# To see your test secret API key embedded in code samples, sign in to your Stripe account.
# You can also find your test secret API key at https://dashboard.stripe.com/test/apikeys.
stripe.api_key = 'sk_test_51PnJGS2LucV5q4G28sO8MrOsoODnyxSQ3D7TpxVV1t7viTRfGAbiHaCvLQjUVeCwdeX1F6veDDJYLVm1olYeuwLz00XDwZEsjq'

stripe_bp = Blueprint('stripe', __name__, url_prefix='/stripe')

YOUR_DOMAIN = 'http://localhost:3003'


@stripe_bp.route('/', methods=['GET'])
def get_index():
    return current_app.send_static_file('index.html')


@stripe_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        price_id = request.form.get('priceId')

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=YOUR_DOMAIN + '/checkout?success=true&session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/checkout?canceled=true',
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        print(e)
        return "Server error", 500


@stripe_bp.route('/create-portal-session', methods=['POST'])
def customer_portal():
    # For demonstration purposes, we're using the Checkout session to retrieve the customer ID.
    # Typically this is stored alongside the authenticated user in your database.
    checkout_session_id = request.form.get('session_id')
    checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

    # This is the URL to which the customer will be redirected after they are
    # done managing their billing with the portal.
    return_url = YOUR_DOMAIN

    customer_email = checkout_session.customer_email
    customer_id = checkout_session.customer

    portalSession = stripe.billing_portal.Session.create(
        customer=checkout_session.customer,
        return_url=return_url,
    )
    return redirect(portalSession.url, code=303)


@stripe_bp.route('/webhook', methods=['POST'])
def webhook_received():
    # Replace this endpoint secret with your endpoint's unique secret
    # If you are testing with the CLI, find the secret by running 'stripe listen'
    # If you are using an endpoint defined with the API or dashboard, look in your webhook settings
    # at https://dashboard.stripe.com/webhooks
    webhook_secret = 'whsec_12345'
    signature = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
        data = event['data']
    except Exception as e:
        return e

    request_data = json.loads(request.data)

    print(request_data)
    print(request.headers)

    data_object = request_data['data']['object']
    event_type = request_data['type']

    if event_type == 'checkout.session.completed':
        customer_email = data_object['email']
        customer_id = data_object['customer']
    elif event_type == 'customer.subscription.created':
        # customer_id data_object.customer
        print('Subscription created %s')
    elif event_type == 'customer.subscription.deleted':
        print('Subscription created %s')
    elif event_type == 'invoice.created':
        customer_email = data_object['email']
        customer_id = data_object['customer']
    elif event_type == 'invoice.payment_succeeded':
        customer_email = data_object['email']
        customer_id = data_object['customer']
    elif event_type == 'invoice.payment_failed':
        customer_email = data_object['email']
        customer_id = data_object['customer']
    elif event_type == 'invoice.paid':
        customer_email = data_object['email']
        customer_id = data_object['customer']

    return jsonify({'status': 'success'})

    # if webhook_secret:
    #     # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
    #     signature = request.headers.get('Stripe-Signature')
    #     try:
    #         event = stripe.Webhook.construct_event(
    #             payload=request.data, sig_header=signature, secret=webhook_secret)
    #         data = event['data']
    #     except Exception as e:
    #         return e
    #     # Get the type of webhook event sent - used to check the status of PaymentIntents.
    #     event_type = event['type']
    # else:
    #     data = request_data['data']
    #     event_type = request_data['type']
    # data_object = data['object']
    #
    #
    #
    # print('event ' + event_type)
    # print(data_object)
    #
    # if event_type == 'checkout.session.completed':
    #     # customer_email data_object.customer_email
    #     # customer_id data_object.customer
    #     print('🔔 Payment succeeded!')
    # elif event_type == 'customer.subscription.trial_will_end':
    #     print('Subscription trial will end')
    # elif event_type == 'customer.subscription.created':
    #     # customer_id data_object.customer
    #     print('Subscription created %s', event.id)
    # elif event_type == 'customer.subscription.updated':
    #     print('Subscription created %s', event.id)
    # elif event_type == 'customer.subscription.deleted':
    #     # handle subscription canceled automatically based
    #     # upon your subscription settings. Or if the user cancels it.
    #     print('Subscription canceled: %s', event.id)
    # elif event_type == 'entitlements.active_entitlement_summary.updated':
    #     # handle active entitlement summary updated
    #     print('Active entitlement summary updated: %s', event.id)

    return jsonify({'status': 'success'})
