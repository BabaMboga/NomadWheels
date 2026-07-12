const apiService ={
    get: async function (url: string) {
        console.log('get', url)

        return new Promise((resolve, reject) => {
            console.log("NEXT_PUBLIC_API_HOST", process.env.NEXT_PUBLIC_API_HOST);
            fetch(`${process.env.NEXT_PUBLIC_API_HOST}${url}`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                }
            })
                .then(response => response.json())
                .then((json) => {
                    console.log('Response:', json)

                    resolve(json)
                })
                .catch((error => {
                    console.log('Error', error)
                    reject(error);
                }))
        })
    }

};

export default apiService