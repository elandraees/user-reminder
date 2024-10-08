
import React, { useState } from 'react';

interface IProductCard {
    title: string;
    price: string;
    subTitle: string;
    productId: string;
    isPopular: boolean;
    useFreeButton: boolean;
    info: string[];
    setProductDetails: (productId: string) => void;

}

const ProductCard = (props: IProductCard) => {


    const handleClick = () => {
        props.setProductDetails(props.productId);
    };

    const greenTick = <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                            fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                            stroke-linejoin="round" className="flex-shrink-0 w-6 h-6 text-emerald-500" aria-hidden="true">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>

    return (


        <div className="relative p-8  border border-gray-200 rounded-2xl shadow-sm flex flex-col">
            <div className="flex-1">
                <h3 className="text-xl font-semibold ">{props.title}</h3>
                {
                    props.isPopular ?
                    <p className="absolute top-0 py-1.5 px-4 bg-emerald-500 text-white rounded-full text-xs font-semibold uppercase tracking-wide  transform -translate-y-1/2">
                    Most popular</p> : ""
                }
                <p className="mt-4 flex items-baseline ">
                    <span className="text-5xl font-extrabold tracking-tight">{props.price}</span><span className="ml-1 text-xl font-semibold">/month</span>
                </p>
                <p className="mt-6 ">{props.subTitle}</p>
                <ul role="list" className="mt-6 space-y-6">
                    {
                        props.info.map(item => {
                            return (
                            <li className="flex">
                                {greenTick}
                                <span className="ml-3 ">{item}</span>
                            </li> 
                            );
                        })
                    }

                </ul>
            </div>
            {
                props.useFreeButton ? 
                <a className="bg-emerald-50 text-emerald-700 hover:bg-emerald-100 mt-8 block w-full py-3 px-6 border border-transparent rounded-md text-center font-medium"
                href="#" onClick={handleClick}>Signup for free</a>
                :
                <a
                className="bg-emerald-500 text-white  hover:bg-emerald-600 mt-8 block w-full py-3 px-6 border border-transparent rounded-md text-center font-medium"
                href="#" onClick={handleClick}>Signup</a>
            }
        </div>

        
    )
}

export default ProductCard