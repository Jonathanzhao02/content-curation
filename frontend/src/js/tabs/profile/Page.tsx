//Importing from outside the project
import React from "react"
import Button from "@material-ui/core/Button"
import Typography from "@material-ui/core/Typography"

//Importing from other files in the project
import { useCCSelector, useCCDispatch } from '../../hooks';
import { logout, show_toast } from "../../state/global"

export default () => {
    const dispatch = useCCDispatch()
    const user = useCCSelector(state => state.global.user)
    

    return <div style={{ marginTop: "4em", marginLeft: "8em" }}>
        {user.username ? <>
            <Typography>Hello, {user.username}! 👋</Typography>
            <Typography>email: {user.email}</Typography>
            <Typography>Your Groups: {user.groups.join(", ")}</Typography>
            <Button onClick={_ => dispatch(logout())}>
                LOGOUT
            </Button>
            {user.groups.includes("Admin") ?
                <Button href="/admin/">
                    Admin Site
                </Button> : <></>
            }
        </> : <>
            <Button href="/accounts/google/login/">
                Login
            </Button>
        </>}
        <Button onClick={() => dispatch(show_toast("Message to display"))} > Test Button </Button>
    </div>
}
