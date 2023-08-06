get:
    create main event

    get pend table for host or create one
    get data table for host or create dummy

    with pend table lock
        for each oid in the request
            if not refresh
                if pending
                    continue

                if found in cache
                    grab cached result
                    continue

            add main event to the pend table
            add oid to request

    if there are oids to be sent
        construct message
        add message to requests table
        send message

    if an oid had an error
        raise it now

    if not waiting for response
        return the values you do have

    wait for all events

    with data table read lock
        for each oid
            grab the value
            - make sure it is present
            - make sure there are no errors

    return the values

listen thread:
    check port number
    decode message
    pull request id
    find the corresponding request
    make sure it has the right number of varbinds
    remove request from table
    check error status

    with data table write lock
        get/create entry for host
        for each varbind
            give it the error found in the request error field
            find the oid requested
            make sure it matches the request
            save varbind to data table

    set the request event

monitor thread:
    wait for next stale request, done, or 1 second (whichever comes first)
    grab next request
    if it is stale
        if it has not timed out
            resend it
        else
            set varbind error to timeout
            signal event
