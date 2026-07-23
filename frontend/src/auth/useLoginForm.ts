import { useState, type FormEvent } from 'react';

import { validateLogin, type LoginData, type LoginErrors } from './validation';

interface UseLoginFormResult {
  email: string;
  password: string;
  errors: LoginErrors;
  setEmail: (value: string) => void;
  setPassword: (value: string) => void;
  handleSubmit: (event: FormEvent<HTMLFormElement>) => void;
}

export function useLoginForm(onSubmit: (data: LoginData) => void): UseLoginFormResult {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<LoginErrors>({});

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const nextErrors = validateLogin({ email, password });
    setErrors(nextErrors);

    if (Object.keys(nextErrors).length === 0) {
      onSubmit({ email, password });
    }
  }

  return { email, password, errors, setEmail, setPassword, handleSubmit };
}
