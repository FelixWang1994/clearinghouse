"""
<Program Name>
  forms.py

<Started>
  October, 2008

<Author>
  Ivan Beschastnikh
  ivan@cs.washington.edu
  
  Jason Chen
  jchen@cs.washington.edu

  Sai Kaushik Borra
  skb386@nyu.edu
<Purpose>

<Usage>
  For more information on forms in django see:
  http://docs.djangoproject.com/en/dev/topics/forms/
"""


from clearinghouse.website.control.models import GeniUser

# from control.models import GeniUser, Sensor, SensorAttribute, ExperimentInfo, ExperimentSensor, ExperimentSensorAttribute


from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
import django.forms as forms



from clearinghouse.common.exceptions import *
from clearinghouse.common.util import validations
from clearinghouse.website.control import interface


MAX_PUBKEY_UPLOAD_SIZE = 2048

class PubKeyField(forms.FileField):

  def clean(self,value,initial):
    forms.FileField.clean(self,value,initial)
    if value is None:
      return None
    if value.size > MAX_PUBKEY_UPLOAD_SIZE:
      raise forms.ValidationError, "Public key too large, file size limit is " + str(MAX_PUBKEY_UPLOAD_SIZE) + " bytes"
    # get the pubkey out of the uploaded file
    pubkey = value.read()
    try:
      validations.validate_pubkey_string(pubkey)
    except ValidationError, err:
      raise forms.ValidationError, str(err)
    return pubkey


class RegisterExperimentForm(forms.Form):

  exp_name = forms.CharField(label="Experiment name", error_messages={'required': 'Enter a experiment name'})
  res_name = forms.CharField(label="Researcher name", error_messages={'required': 'Enter a researcher name'})
  res_address = forms.CharField(label="Name and address of researcher's home institution", error_messages={'required': 'Enter a Name and address of researchers home institution'})
  res_email = forms.CharField(label="Researcher's email address", widget=forms.EmailInput(attrs={'class': 'form-control','pattern': "(?!(^[.-].*|[^@]*[.-]@|.*\.{2,}.*)|^.{254}.)([a-zA-Z0-9!#$%&'*+\/=?^_`{|}~.-]+@)(?!-.*|.*-\.)([a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,15}"}), error_messages={'required': 'Enter an E-mail Address'})
  irb = forms.CharField(label="Name of home institution's IRB officer or contact person", error_messages={'required': 'Name of home institutions IRB officer or contact person'})
  irb_email = forms.CharField(label="Email address of of home institution's IRB officer or contact person", widget=forms.EmailInput(attrs={'class': 'form-control','pattern': "(?!(^[.-].*|[^@]*[.-]@|.*\.{2,}.*)|^.{254}.)([a-zA-Z0-9!#$%&'*+\/=?^_`{|}~.-]+@)(?!-.*|.*-\.)([a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,15}"}), error_messages={'required': 'Enter an E-mail Address'})
  goal = forms.CharField(label="What is the goal of your research experiment? What do you want to find out?",widget=forms.Textarea(attrs={'class': 'form-control', 'rows':1,'placeholder': 'Enter the goal of your Experiment'}),error_messages={'required': 'Enter the goal of your research experiment'}, max_length=256)

  def clean_exp_name(self):
    value = self.cleaned_data['exp_name']
    try:
      validations.validate_register_experiment_field(value)
    except ValidationError, err:
      raise forms.ValidationError, str(err)
    return value

  def clean_res_name(self):
    value = self.cleaned_data['res_name']
    try:
      validations.validate_register_experiment_field(value)
    except ValidationError, err:
      raise forms.ValidationError, str(err)
    return 

  def clean_res_address(self):
    value = self.cleaned_data['res_address']
    try:
      validations.validate_register_experiment_field(value)
    except ValidationError, err:
      raise forms.ValidationError, str(err)
    return value

  def clean_res_email(self):
    value = self.cleaned_data['res_email']
    try:
      validations.validate_email(value)
    except ValidationError, err:
      raise forms.ValidationError, str(err)
    return value

  def clean_irb(self):
    value = self.cleaned_data['irb']
    try:
      validations.validate_register_experiment_field(value)
    except ValidationError, err:
      raise forms.ValidationError, str(err)
    return

  def clean_irb_email(self):
    value = self.cleaned_data['irb_email']
    try:
      validations.validate_email(value)
    except ValidationError, err:
      raise forms.ValidationError, str(err)
    return value

  def clean_res_goal(self):
    value = self.cleaned_data['goal']
    try:
      validations.validate_register_experiment_field(value)
    except ValidationError, err:
      raise forms.ValidationError, str(err)
    return



class SensorListForm(forms.Form):
  TRUE_FALSE_CHOICES = {
    (True, "Yes"),
    (False, "No")
  }
  battery = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="Battery",  widget=forms.Select(), required=True)
  bluetooth = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="Bluetooth",  widget=forms.Select(), required=True)
  cellular = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="Cellular",  widget=forms.Select(), required=True)
  location = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="Location",  widget=forms.Select(), required=True)
  settings = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="Settings",  widget=forms.Select(), required=True)
  sensor = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="Sensor",  widget=forms.Select(), required=True)
  signalstrenght = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="Signal strenght",  widget=forms.Select(), required=True)
  wifi = forms.ChoiceField(choices = TRUE_FALSE_CHOICES, label="Wifi",  widget=forms.Select(), required=True)



  def clean_data(self):
    
    battery = self.cleaned_data['battery']
    bluetooth = self.cleaned_data['bluetooth']
    cellular = self.cleaned_data['cellular']
    location = self.cleaned_data['location']
    settings = self.cleaned_data['settings']
    sensor = self.cleaned_data['sensor']
    signalstrenght = self.cleaned_data['signalstrenght']
    wifi = self.cleaned_data['wifi']

    return [{'battery': battery}, {'bluetooth': bluetooth}, {'cellular': cellular}, {'location': location}, {'settings': settings}, {'sensor': sensor}, {'signalstrenght': signalstrenght}, {'wifi': wifi}]



class RegisterExperimentSensorForm(forms.Form):

  
  frequency = forms.IntegerField(label='Once every', min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
  F_CHOICES = (('hour', 'Hour'),('min', 'Min'),('sec', 'Sec'),)
  frequency_unit = forms.ChoiceField(widget = forms.Select(attrs={'class': 'form-control'}),
                   choices = F_CHOICES, initial='hour', required = True,)
  frequency_other = forms.CharField(label="Other:", required=False,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Please provide any additional information that you would like'}))
  usage_policy = forms.CharField(label='What will these sensor data be used for?',widget=forms.Textarea(attrs={'class': 'form-control', 'rows':1,'placeholder': 'Enter how do you plan to use the collected data'}),max_length=512)
  P_CHOICES = (('full', 'Full Precision'),('truncate', 'Truncate'),)
  precision_choice = forms.ChoiceField(widget = forms.Select(),
             choices = P_CHOICES, required = False,)
  precision_other = forms.CharField(label="A level of data precision that we currently do not support? Please elaborate:", required=False,widget=forms.Textarea(attrs={'class': 'form-control', 'rows':1, 'placeholder': 'Please provide any additional information that you would like'}))
  s_goal = forms.CharField(label="What will this sensor used for?",widget=forms.Textarea(attrs={'class': 'form-control', 'rows':1,'placeholder': 'Enter the goal of your Experiment'}),error_messages={'required': 'Enter the goal of your research experiment'}, max_length=256)


class BatteryForm(forms.Form):
  if_battery_present = forms.BooleanField(label="if_battery_present")
  battery_health = forms.BooleanField(label="battery_health")
  battery_level = forms.BooleanField(label="battery_label")
  battery_plug_type = forms.BooleanField(label="battery_plug_type")
  battery_status = forms.BooleanField(label="battery_status")
  battery_technology = forms.BooleanField(label="battery_technology")

class BluetoothForm(forms.Form):
  bluetooth_state = forms.BooleanField(label="bluetootyh_state (if Bluetooth is enabled")
  bluetooth_is_discovering = forms.BooleanField(label="bluetooth_is_discovering (if the local Bluetooth adapter is currently in device discovery process)")
  scan_mode = forms.BooleanField(label="scan_mode (if Bluetooth is connectable or discoverable")
  local_address = forms.BooleanField(label="local_address (hardware address of the local Bluetooth adapter)")
  local_name = forms.BooleanField(label="local_name (visible device name)")

class CellularForm(forms.Form):
  network_roaming = forms.BooleanField(label="network_roaming (returns true if the device is considered roaming on the current network, for GSM purposes)")
  cellID = forms.BooleanField(label="cellID (details about  cell ID) ")
  network_roaming = forms.BooleanField(label="location_area_code")
  location_area_code = forms.BooleanField(label="mobile_country_code (mobile country code, or MCC)")
  mobile_country_code = forms.BooleanField(label="mobile_network_code (mobile network code, or MNC)")
  mobile_network_code = forms.BooleanField(label="network_operator (returns the numeric name, MCC+MNC, of current registered operator. Note: MCC+MNC  identify a unique operator) ")
  network_operator = forms.BooleanField(label="network_operator_name (returns the alphabetic name of current registered operator)")
  network_type = forms.BooleanField(label="network_type (returns the radio technology, or network type, currently in use on the device)")
  service_state = forms.BooleanField(label="service_state (returns the state of cellular service: emergency call only, in service, out of service, or power off)")
  signal_strengths = forms.BooleanField(label="signal_strengths")

class LocationForm(forms.Form):
  location_providers = forms.BooleanField(label="location_providers (network/GPS/passive)")
  location_provider_enabled = forms.BooleanField(label="location_provider_enabled (check if one of the providers is enabled)")
  location = forms.BooleanField(label="location")
  last_known_location = forms.BooleanField(label="location")
  geocode = forms.BooleanField(label="geocode (obtain a list of addresses for the given latitude and longitude)")

class SettingsForm(forms.Form):
  airplane_mode = forms.BooleanField(label="airplane_mode")
  ringer_silent_mode = forms.BooleanField(label="ringer_silent_mode")
  screen_on = forms.BooleanField(label="screen_on")
  max_media_volume = forms.BooleanField(label="max_media_volume")
  max_ringer_volume = forms.BooleanField(label="max_ringer_volume")
  media_volume = forms.BooleanField(label="media_volume")
  ringer_volume = forms.BooleanField(label="ringer_volume")
  screen_brightness = forms.BooleanField(label="screen_brightness")
  screen_timeout = forms.BooleanField(label="screen_timeout")

class SensorForm(forms.Form):
  sensor = fprms.BooleanField(label="sensors (get the most recently recorded sensor data: accelerometer, magnetic and orientation)")
  sensors_accuracy = fprms.BooleanField(label="sensors_accuracy")
  light = fprms.BooleanField(label="light (most recently received light value)")
  accelerometer = fprms.BooleanField(label="accelerometer (most recently received accelerometer value)")
  magnetoneter = fprms.BooleanField(label="magnetometer (most recently received magnetic field value)")
  orientation = fprms.BooleanField(label="orientation (most recently received orientation value)")

class SignalStrengthForm(forms.Form):
  signal_strengths = forms.BooleanField(label="signal_strengths")


class WifiForm(forms.Form):
  wifi_state = forms.BooleanField(label="wifi_state (check WiFi state: whether it is enabled)")
  ip_address = forms.BooleanField(label="ip_address")
  link_speed = forms.BooleanField(label="link_speed")
  supplicant_state = forms.BooleanField(label="supplicant_state (scanning, associating, completed, etc.)")
  ssid = forms.BooleanField(label="ssid")
  rssi = forms.BooleanField(label="rssi (received signal strength indicator)")
  scan_results = forms.BooleanField(label="scan_results (list of access points found during the most recent WiFi scan: list of information similar to connectionInfo)")


class GeniUserCreationForm(DjangoUserCreationForm):

  affiliation = forms.CharField(error_messages={'required': 'Enter an Affiliation'})
  email = forms.CharField(label="E-mail Address", error_messages={'required': 'Enter an E-mail Address'})
  pubkey = PubKeyField(label="My Public Key", required=False)
  gen_upload_choice = forms.ChoiceField(label="", choices=((1, 'Generate key pairs for me'), (2, 'Let me upload my public key')))
  username = forms.CharField(label="Username", error_messages={'required': 'Enter a username'}, max_length=validations.USERNAME_MAX_LENGTH)
  
  def __init__(self, *args):
    DjangoUserCreationForm.__init__(self, *args)
    #self.fields['username'].error_messages['required'] = 'Enter a username'
    self.fields['password1'].error_messages['required'] = 'Enter a password'
    self.fields['password2'].error_messages['required'] = 'Verify your password'

  def clean_username(self):
    value = self.cleaned_data['username']
    try:
      validations.validate_username(value)
    except ValidationError, err:
      raise forms.ValidationError, str(err)
    return value
  
  def clean_password1(self):
    value = self.cleaned_data['password1']
    try:
      validations.validate_password(value)
    except ValidationError, err:
      raise forms.ValidationError, str(err)
    return value
  
  def clean_affiliation(self):
    value = self.cleaned_data['affiliation']
    try:
      validations.validate_affiliation(value)
    except ValidationError, err:
      raise forms.ValidationError, str(err)
    return value
  
  def clean_email(self):
    value = self.cleaned_data['email']
    try:
      validations.validate_email(value)
    except ValidationError, err:
      raise forms.ValidationError, str(err)
    return value




def gen_edit_user_form(field_list='__all__', *args, **kwargs):
  """
  <Purpose>
      Dynamically generates a EditUserForm depending on field_list.

  <Arguments>
      field_list:
          The profile view passes in the desired field that will be edited by the
          EditUserForm.

  <Exceptions>
      ValidationErrors raised by a incorrect field value.

  <Side Effects>
      None.

  <Returns>
      A EditUserForm object that is specific to the field list passed in.

  """
  class EditUserForm(forms.ModelForm):
    class Meta:
      model = GeniUser
      fields = field_list
      
    def __init__(self):
      super(EditUserForm, self).__init__(*args, **kwargs)
      
    def clean_affiliation(self):
      value = self.cleaned_data['affiliation']
      try:
        validations.validate_affiliation(value)
      except ValidationError, err:
        raise forms.ValidationError, str(err)
      return value
      
    def clean_email(self):
      value = self.cleaned_data['email']
      try:
        validations.validate_email(value)
      except ValidationError, err:
        raise forms.ValidationError, str(err)
      return value
    
  return EditUserForm()





class EditUserPasswordForm(forms.ModelForm):
  password1 = forms.CharField(label=("Password"), required=False, widget=forms.PasswordInput)
  password2 = forms.CharField(label=("Password confirmation"), required=False, widget=forms.PasswordInput, help_text = ("Enter the same password as above, for verification."))
  class Meta:
    model = GeniUser
    fields = ('password1','password2')
    
  def clean(self):
    data = self.cleaned_data
    if data['password1'] != data['password2']:
      raise forms.ValidationError(("The two password fields didn't match."))
    try:
      validations.validate_password(data['password1'])
    except ValidationError, err:
      raise forms.ValidationError, str(err)
    return data






class AutoRegisterForm(forms.ModelForm):
  username = forms.CharField(label="Username", error_messages={'required': 'Enter a username'}, max_length=validations.USERNAME_MAX_LENGTH)
  class Meta:
    model = GeniUser
    fields = ('username',)

  def clean_username(self):
    value = self.cleaned_data['username']
    try:
      validations.validate_username(value)
    except ValidationError, err:
      raise forms.ValidationError, str(err)
    return value
  
  '''    
  def clean(self):
    data = self.cleaned_data
    try:
      validations.validate_username(data['username'])
    except ValidationError, err:
      raise forms.ValidationError, str(err)
    return data    
  '''    





def gen_get_form(geni_user, req_post=None):
  """
  <Purpose>
      Dynamically generates a GetVesselsForm that has the right
      number vessels (the allowed number of vessels a user may
      acquire). Possibly generate a GetVesselsForm from an HTTP POST
      request.

  <Arguments>
      geni_user:
          geni_user object
      req_post:
          An HTTP POST request (django) object from which a
          GetVesselsForm may be instantiated. If this argument is
          not supplied, a blank form will be created

  <Exceptions>
      None.

  <Side Effects>
      None.

  <Returns>
      A GetVesselsForm object that is instantiated with a req_post
      (if given).
  """
      
  # the total number of vessels a user may acquire
  avail_vessel_credits = interface.get_available_vessel_credits(geni_user)
  
  # Dynamic generation of the options for numbers the user can request based
  # on their number of available vessel credits.
  if avail_vessel_credits == 0:
    step = [0]
  elif avail_vessel_credits < 10:
    step = range(1, avail_vessel_credits+1)
  elif avail_vessel_credits < 100:
    step = range(1, 10)
    step.extend(range(10, avail_vessel_credits+1,10))
  else:
    step = range(1, 10)
    step.extend(range(10, 101,10))
    step.extend(range(200, avail_vessel_credits+1, 100))
    
  if avail_vessel_credits not in step:
    step.append(avail_vessel_credits)

  # dynamically generate the get vessels form
  #get_vessel_choices = zip(range(1,max_num+1),range(1,max_num+1))
  get_vessel_choices = zip(step, step)
  
  # This is ugly (nested class definition, that is) and appears to have been
  # done as a way to avoid using a constructor but still make the value of
  # get_vessel_choices available to instances of this class.
  class GetVesselsForm(forms.Form):
    """
    <Purpose>
        Generates a form to acquire vessels by the user
    <Side Effects>
        None
    <Example Use>
        GetVesselsForm()
            to generate a blank form
        GetVesselsForm(post_request)
            to generate a form from an existing POST request
    """
    # maximum number of vessels a user is allowed to acquire
    #num = forms.ChoiceField(choices=get_vessel_choices, error_messages={'required' : 'Please enter the number of vessels to acquire'})
    num = forms.ChoiceField(choices=get_vessel_choices)
    
    # the various environment types the user may select from
    #env = forms.ChoiceField(choices=((1,'LAN'),(2,'WAN'),(3,'Random')), error_messages={'required' : 'Please enter the networking environment for vessels to acquire'})
    env = forms.ChoiceField(choices=(('wan','WAN'),('lan','LAN'),('nat','NAT'),('rand','Random')))
    
    def clean_num(self):
      value = int(self.cleaned_data['num'])
      if value < 1:
        raise forms.ValidationError("Invalid vessel number selection.")
      return value
    
    def clean_env(self):
      value = str(self.cleaned_data['env'])
      if not (value == 'wan' or value == 'lan' or value == 'nat' or value == 'rand'):
        raise forms.ValidationError("Invalid vessel type selection.")
      return value
    
    def get_errors_as_str(self):
      return str(self.errors)
  
  if req_post is None:
      return GetVesselsForm()
  return GetVesselsForm(req_post)
