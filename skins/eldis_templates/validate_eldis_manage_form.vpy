## Controlled Python Script "validate_eldis_manage_form"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Validates eldis manage form
##

if state.getErrors():
    return state.set(status='failure', portal_status_message='Please correct the indicated errors.')
return state