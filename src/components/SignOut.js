import React from 'react'
import { auth } from '../Firebase'
function SignOut() {

    return (
        <div>
            <button onClick={() => auth.signOut()} type="button" class="text-white bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 hover:bg-gradient-to-br focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2">Sign Out</button>
        </div>
    )
}

export default SignOut