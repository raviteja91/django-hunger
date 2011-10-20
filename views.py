from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from beta.models import InvitationCode
from beta.forms import InviteRequestForm

def verify_invite(request, invitation_code):
    try:
        invitation_code = InvitationCode.objects.get(code=invitation_code)
        
        if inivitation_code.is_user:
            #already used
            return HttpResponseRedirect(reverse('beta_expired'))
        else:
            request.session.['in_beta'] = True
            url = getattr(settings, 'BETA_SIGNUP_URL', '/signup/')
            return redirect(url)
    except InvitationCode.DoesNotExist:
        url = getattr(settings, 'BETA_REDIRECT_URL', '/beta/')
        return redirect(url)


def invite(request, form_class=InviteRequestForm, template_name="beta/request_invite.html", extra_context=None):
    """
    Allow a user to request an invite at a later date by entering their email address.
    
    **Arguments:**
    
    ``template_name``
        The name of the tempalte to render.  Optional, defaults to
        privatebeta/invite.html.

    ``extra_context``
        A dictionary to add to the context of the view.  Keys will become
        variable names and values will be accessible via those variables.
        Optional.
    
    **Context:**
    
    The context will contain an ``InviteRequestForm`` that represents a
    :model:`invitemelater.InviteRequest` accessible via the variable ``form``.
    If ``extra_context`` is provided, those variables will also be accessible.
    
    **Template:**
    
    :template:`privatebeta/invite.html` or the template name specified by
    ``template_name``.
    """
    form = form_class(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('beta_confirmation'))

    context = {'form': form}

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template_name, context,
        context_instance=RequestContext(request))

def confirmation(request, template_name="beta/confirmation.html", extra_context=None):
    """
    Display a message to the user after the invite request is completed
    successfully.
    
    **Arguments:**
    
    ``template_name``
        The name of the tempalte to render.  Optional, defaults to
        privatebeta/sent.html.

    ``extra_context``
        A dictionary to add to the context of the view.  Keys will become
        variable names and values will be accessible via those variables.
        Optional.
    
    **Context:**
    
    There will be nothing in the context unless a dictionary is passed to
    ``extra_context``.
    
    **Template:**
    
    :template:`privatebeta/sent.html` or the template name specified by
    ``template_name``.
    """
    return direct_to_template(request, template=template_name, extra_context=extra_context)
    

def expired(request, template_name="beta/expired.html", extra_context=None):
    """
    Display a message to the user that the invitation code has already been used.
    
    **Arguments:**
    
    ``template_name``
        The name of the tempalte to render.  Optional, defaults to
        privatebeta/sent.html.

    ``extra_context``
        A dictionary to add to the context of the view.  Keys will become
        variable names and values will be accessible via those variables.
        Optional.
    
    **Context:**
    
    There will be nothing in the context unless a dictionary is passed to
    ``extra_context``.
    
    **Template:**
    
    :template:`privatebeta/sent.html` or the template name specified by
    ``template_name``.
    """
    return direct_to_template(request, template=template_name, extra_context=extra_context)