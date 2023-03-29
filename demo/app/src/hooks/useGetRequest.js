import { useState } from "react";

const useGetRequest = () => {
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState("");

    fetch("/api/products")
    .then((res) => {
        res.json();
        console.log(res);
    })
    .then((data) => {
        console.log(data)
        setData(data)
        setIsLoading(false)
    }).catch(e => setError(e));
    
    return { data, isLoading, error };
};
    
export default useGetRequest;
