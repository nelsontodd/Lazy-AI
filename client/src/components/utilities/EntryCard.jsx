import React, { useState } from 'react';
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTrashCan } from '@fortawesome/free-solid-svg-icons';

import Card from './Cards/Card';
import CardBody from './Cards/CardBody';

import { getCookies } from '../../helpers/setAuthToken';

const EntryCard = (props) => {
    const id = useState(props.entry._id)[0];
    const body = useState(props.entry.body)[0];
    const createdAt = useState(props.entry.createdAt)[0];

    const onClick = async (e) => {
        e.preventDefault();
        try {
            const token = getCookies().token;
            const headers = {
                'x-auth-token': token
            };
            await axios.delete(`/api/entries/${id}`, {
                    headers: headers
                }
            );
            window.location.reload(true);
        } catch (err) {
            const errorMessage  = err.response.data.errors[0].msg;
            alert(errorMessage);
        }
    }

    return (
        <Card key={id}>
            <CardBody>
                <h5>{body}</h5>
                <p>
                    {createdAt.toLocaleDateString()}
                </p>
                <FontAwesomeIcon
                    icon={faTrashCan}
                    onClick={(e) => onClick(e)}
                />
            </CardBody>
        </Card>
    );
}

export default EntryCard;
