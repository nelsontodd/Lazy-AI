import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import axios from 'axios';

import Container from "./utilities/Container";

import { getCookies, isLoggedIn } from '../helpers/setAuthToken';

const Entry = () => {

    let history = useHistory();
    const [entry, setEntry] = useState('');

    const onChange = (e) => {
        let value = e.target.value
        if (value.length <= 280) {
            setEntry(value);
        }
    }

    const onSubmit = async (e) => {
        e.preventDefault();
        const formData = {
            'body': entry
        };
        try {
            const token = getCookies().token;
            const headers = {
                'x-auth-token': token
            };
            await axios.post('/api/entries', formData, {
                    headers: headers
                }
            );
            setEntry('');
            history.push('/journal');
        } catch (err) {
            const errorMessage  = err.response.data.errors[0].msg;
            alert(errorMessage);
        }
    }

    if (!isLoggedIn()) {
        history.push('/login')
        return null;
    } else {
        return (
            <Container>
                <form onSubmit={onSubmit}>

                    <label className="lead">
                        Make your entry here:
                    </label>
                    <textarea
                        type="text"
                        className="u-full-width"
                        name="entry"
                        placeholder="Today I..."
                        value={entry}
                        onChange={(e) => onChange(e)}
                        required
                    />

                    <input
                        className="button button-primary"
                        type="submit"
                        value="Save Entry"
                    />

                </form>
                <a className="button" href="/journal">Cancel</a>
            </Container>
        );
    }
}

export default Entry;
