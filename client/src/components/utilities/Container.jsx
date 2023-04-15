import React from 'react';


const Container = ({ children }) => {
    return (
        <div className="container content">
            { children }
        </div>
    );
}

export default Container;
