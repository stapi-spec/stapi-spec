import { useEffect, useState } from "react";
import useLocalStorage from "./useLocalStorage";
import { ALL_PROVIDERS } from "src/utils/constants";

const useGetProducts = () => {
    const [data, setData] = useState({});
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState("");
    const { userToken } = useLocalStorage();

    useEffect(() => {
        const allProductRequests = ALL_PROVIDERS.map(async provider => {
            return fetch('/api/products', {headers: new Headers({
                'Backend': provider.id,
                'Authorization': `Bearer ${userToken}`
            })})
            .then(async res => await res.json())
            .then(data => { return {'provider': provider.id, 'data': data}})
        });

        Promise.all(allProductRequests).then((results) => {
            setData(Object.fromEntries(Object.values(results).map(value => {
                return [value.provider, value.data.products]
            })));
            setIsLoading(false)
        }).catch(e => setError(e));

    }, []);

    return { data, isLoading, error };
};

export default useGetProducts;
