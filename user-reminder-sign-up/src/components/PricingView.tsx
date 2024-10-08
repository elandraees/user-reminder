
import React, { useState } from 'react';
import ProductCard from './ProductCard';

interface IPricingViewProps {
    setProductId: React.Dispatch<React.SetStateAction<string>>;
    setStepId: React.Dispatch<React.SetStateAction<number>>;
}

const PricingView = (props: IPricingViewProps) => {

    const setProductDetails = (productId: string) => {
        props.setProductId(productId)
        props.setStepId(1)
    };


    return (

        <div className="">

            <div>
                <h2 className="text-3xl font-bold tracki text-center mt-12 sm:text-5xl ">Pricing</h2>
                <p className="max-w-3xl mx-auto mt-4 text-xl text-center ">Get started on our free plan and upgrade when you are ready.</p>
            </div>

            <div className="mt-24 container space-y-12 lg:space-y-0 lg:grid lg:grid-cols-2 lg:gap-x-8 m-auto mt-10">

                <ProductCard isPopular={false} setProductDetails = {setProductDetails} useFreeButton={true} productId="1" title='Free' price='$0' subTitle='Create notifications using your browser storage' info={['10 credits', 'Free']}/>

                <ProductCard isPopular={true} setProductDetails = {setProductDetails} useFreeButton={false} productId="price_1PnJIv2LucV5q4G2Th2V6QJM" title='Pro' price='$1' subTitle='Create notifications using your browser storage' info={['20 credits', 'Unlimited Reminders']}/>

            </div>

        </div>
    )
}

export default PricingView