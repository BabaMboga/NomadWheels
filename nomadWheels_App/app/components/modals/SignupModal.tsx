'use client';
import Modal from "./Modal";
import { useState } from "react";
import {useRouter} from "next/navigation";
import useSignupModal from "@/app/hooks/useSignupModal";
import CustomButton from "../forms/CustomButton";
import apiService from "@/app/services/apiService";



const SignupModal = () => {

    //Variables

    const router = useRouter();
    const signupModal = useSignupModal();
    const [email, setEmail] = useState('');
    const [password1,setPassword1] = useState('');
    const [password2, setPassword2] = useState('');
    const [errors, setErrors] = useState<string[]>([]);

    type SignupResponse = {
        access?: string;
        refresh?: string;
        [key: string]: string | string[] | undefined;
    }
    

    // Submit functionality
    const submitSignup = async () => {
        const formData = {
            email: email,
            password1: password1,
            password2: password2
        }

        const response = await apiService.post<SignupResponse>('/api/auth/register', formData);

        if (response.access) {
            // handleLogin

            signupModal.close();

            router.push('/')
        } else {
            // map will return an array of arrays 
            // const tmpErrors = Object.values(response).map((error) => Array.isArray(error) ? error.join(",") : error ?? "")

            //using flatmap instead gives an array of strings
            const tmpErrors: string[] = Object.values(response).flatMap((error) => {
                if (!error) return [];
                return Array.isArray(error) ? error : [error];
            })


            setErrors(tmpErrors);
        }
    }

    const content = (
        <>
            <h2 className="mb-6 text-2xl">Welcome to NomadWheels, plese login</h2>

            <form action={submitSignup} className="space-y-4">
                <input
                    onChange={(e) => setEmail(e.target.value)} 
                    placeholder="Your e-mail address" 
                    type="email" 
                    className="w-full h-[54px] px-4 border border-gray-300 rounded-xl" 
                />
                <input
                    onChange={(e) => setPassword1(e.target.value)} 
                    placeholder="Your password" 
                    type="password" 
                    className="w-full h-[54px] px-4 border border-gray-300 rounded-xl"
                />
                <input
                    onChange={(e) => setPassword2(e.target.value)} 
                    placeholder="Repeat password" 
                    type="password" 
                    className="w-full h-[54px] px-4 border border-gray-300 rounded-xl"
                />

                {errors.map((error, index) => {
                    return (
                        <div key={`error_${index}`} className="p-5 bg-nomadWheels text-white rounded-xl opacity-80">
                            {error}
                        </div>

                    )
                })}

                

                <CustomButton 
                label= "Submit"
                onClick={submitSignup}
                />

            </form>

            
        </>
        

        
    )
    return (
        <Modal 
            isOpen={signupModal.isOpen}
            close={signupModal.close}
            label="SignUp"
            content={content}
        />
    );
}

export default SignupModal;