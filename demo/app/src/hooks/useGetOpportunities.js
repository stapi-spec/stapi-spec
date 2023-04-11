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

    function fetchAllProviderProducts(p){
        return products[p] && products[p].map(async product => {
            return fetchOpportunity(userToken, p, Object.assign(params, {"product_id": product.id})).then(async res => await res.json()).then(data => { return {'provider': p, 'data': data}});
        });
    };

    useEffect(() => {
        if (params) {
            setIsLoading(true);
            setError(false);
            // By default fetch all provider product opportunities
            if(!provider && !params["product_id"]){
                const allProvidersOpportunities = ALL_PROVIDERS.reduce((all, p) => {
                    const promises = fetchAllProviderProducts(p.id);
                    return promises ? [...all, ...promises] : all;
                }, []);

                Promise.all(allProvidersOpportunities).then(results => {
                    setData(Object.fromEntries(Object.values(results).map(value => {
                        return [value.provider, value.data.features]
                    })));
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
