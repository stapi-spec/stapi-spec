import { useEffect, useState } from "react";
import useLocalStorage from "./useLocalStorage";

const useGetRequest = () => {
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState("");
    const { userToken } = useLocalStorage();

    useEffect(() => {
        fetch('/api/products', {headers: new Headers({
            'Backend': 'earthsearch',
            'Authorization': `Bearer ${userToken}`
        })})
        .then((res) => res.json())
        .then((data) => {
            setData(data['products'])
            setIsLoading(false)
        }).catch(e => setError(e));
    }, []);

    return { data, isLoading, error };
};

export default useGetRequest;
