import React from 'react';

import Hello from "./hello.jsx";
import MyApp from "./button.jsx";
import Member from "./member.jsx";

console.log('Load app')

const App = () => {
    
    return (
        <>
        <h1>React</h1>
        <MyApp />
        <Member />
        </>
        
    
    
    );

};
console.log('Load App')

export default App;

