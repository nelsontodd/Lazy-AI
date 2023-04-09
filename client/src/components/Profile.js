import React from 'react';
import { useHistory } from 'react-router-dom';

import { isLoggedIn } from '../utils/setAuthToken';

const Profile = () => {

    let history = useHistory();

    if (!isLoggedIn()) {
        history.push('/login')
        return null;
    } else {
        return (
            <div>
                <p>This is the profile page</p>
            </div>
        );
    }
}

export default Profile;
