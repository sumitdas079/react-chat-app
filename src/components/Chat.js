import React, { useEffect, useState, useRef } from 'react'
import { auth, db } from '../Firebase'
import '../app.css'
import SignOut from './SignOut'
import SendMessage from './SendMessage'
function Chat() {

    const scroll = useRef()
    const [messages, setMessages] = useState([])
    useEffect(() => {
        db.collection('anything').orderBy('createdAt').limit(50).onSnapshot(snapshot => { setMessages(snapshot.docs.map(doc => doc.data())) })
    }, [])

    return (
        <div>
            <SignOut />
            <div className='msgs'>
                {messages.map(({ id, text, photoURL, uid }) =>
                (
                    <div>
                        <div key={id} className={`msg ${uid === auth.currentUser.uid ? 'sent' : 'received'}`}>
                            <img src={photoURL} alt="" />
                            <p>{text}</p>
                        </div>
                    </div>
                ))}
            </div>
            <SendMessage scroll={scroll} />
            <div ref={scroll}></div>
        </div>
    )
}

export default Chat