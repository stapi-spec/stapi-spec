import { useEffect, useState } from "react";
import useLocalStorage from "./useLocalStorage";
import { ALL_PROVIDERS } from "src/utils/constants";

function fetchOpportunity(token, provider, params){
    return fetch("/api/opportunities", {
        method: "POST",
        headers: {
            "Content-type": "application/json",
            "Backend": provider,
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(params)
    });
};

const useGetOpportunities = (products, postParams) => {
    const {params, provider} = !!postParams && postParams;
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");
    const { userToken } = useLocalStorage();

    function setAsyncResultsData(promises){
        Promise.all(promises).then(results => {
            setData(Object.fromEntries(Object.values(results).map(value => {
                return [value.provider, value.data.features]
            })));
            setIsLoading(false);
        }).catch(e => {
            setError(e);
            setIsLoading(false);
        });
    }

    async function fetchByProduct(p, productId){
        return fetchOpportunity(userToken, p, Object.assign(params, {"product_id": productId})).then(async res => await res.json()).then(data => { return {'provider': p, 'data': data}});
    }

    function fetchAllProviderProducts(p){
        return products[p] && products[p].map(async product => {
            return fetchByProduct(p, product.id);
        });
    };

    useEffect(() => {
        if (params) {
            setIsLoading(true);
            setError(false);
            // By default fetch all provider product opportunities
            if(provider === 'all' && params["product_id"] === 'all'){
                const allProvidersOpportunities = ALL_PROVIDERS.reduce((all, p) => {
                    const promises = fetchAllProviderProducts(p.id);
                    return promises ? [...all, ...promises] : all;
                }, []);

                setAsyncResultsData(allProvidersOpportunities);
            }
            else if(provider === 'all'){
                const productOpportunities = ALL_PROVIDERS.reduce((all, p) => {
                    const promise = fetchByProduct(p.id, params["product_id"]);
                    return promise ? [...all, promise] : all;
                }, []);

                setAsyncResultsData(productOpportunities);
            }
            else if(params["product_id"] === 'all'){
                const providerOpportunities = fetchAllProviderProducts(provider)
                setAsyncResultsData(providerOpportunities);
            }
            else{
                fetchOpportunity(userToken, provider, params)
                .then(async res => await res.json())
                .then(data => {
                    setData({[provider]: data.features});
                    setIsLoading(false);
                }).catch(e => {
                    setError(e);
                    setIsLoading(false);
                });
            }
        }
    }, [params, provider]);

    return { data, isLoading, error };
};

export default useGetOpportunities;
