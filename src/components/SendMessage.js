import React, { useState } from 'react'
import { db, auth } from '../Firebase'
import firebase from 'firebase/compat/app'
function SendMessage({ scroll }) {

    const [message, setMessage] = useState('')

    async function sendmessage(e) {
        e.preventDefault()
        const { uid, photoURL } = auth.currentUser
        await db.collection('anything').add({
            text: message, photoURL, uid, createdAt: firebase.firestore.FieldValue.serverTimestamp()
        })
        setMessage('')
        scroll.current.scrollIntoView({ behavior: 'smooth' })
    }

    return (
        <>
            <form onSubmit={sendmessage}>
                <div classNameName="relative flex w-1/3 flex-wrap items-stretch mb-3">
                    <input type="text" value={message} onChange={e => setMessage(e.target.value)} placeholder="Type a Message" className="px-3 py-3 placeholder-blueGray-300 text-blueGray-600 relative bg-white bg-white rounded text-sm border-0 shadow outline-none focus:outline-none focus:ring w-1/3 pr-10" />
                    <button type="submit" className="text-white bg-sky-500 hover:bg-sky-800 focus:ring-4 focus:ring-sky-300 font-medium rounded-full text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:bg-sky-600 dark:hover:bg-sky-700 dark:focus:ring-sky-800">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path fill="none" d="M0 0h24v24H0z" /><path d="M3.741 1.408l18.462 10.154a.5.5 0 0 1 0 .876L3.741 22.592A.5.5 0 0 1 3 22.154V1.846a.5.5 0 0 1 .741-.438zM5 13v6.617L18.85 12 5 4.383V11h5v2H5z" /></svg>
                    </button>
                </div>
            </form>
        </>
    )
}

export default SendMessage