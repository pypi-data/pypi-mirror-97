# PSU_EXPORT

Enables BI/Cognos data export for `psu_base`-enabled apps

## Installation/Configuration

Step 1: Add `psu-export` to requirements.txt

Step 2: Provide secrets in `local_settings.py`, and/or via `eb setenv`
* BI_EXPORT_ACCESS_KEY *- Get from another developer, or from BI team*
* BI_EXPORT_SECRET_KEY *- Get from another developer, or from BI team*

Step 3: Add `psu_export` and `psu_scheduler` to `INSTALLED_APPS` in `settings.py`
```buildoutcfg
INSTALLED_APPS = [
    ...
    'psu_base',
    'psu_export',
    'psu_scheduler',
]
```

Step 4: Add URLS for psu-export and psu-scheduler to urls.py
```
url('export/', include(('psu_export.urls', 'psu_export'), namespace='export')),
url('scheduler/', include(('psu_scheduler.urls', 'psu_scheduler'), namespace='scheduler')),
```

Step 5: Ensure `HOST_URL` is defined in your AWS settings (as required by psu_base). 
The `HOST_URL` setting can be overridden if needed by a setting named `SCHEDULER_URL`

## Define which models are exported

### Your Application
By default, all models in your app will be exported.  You can change this with the `EXPORT_MODELS` 
setting (described below)

### Installed PSU-* Apps
Models within installed psu-* apps will not be exported, unless that psu-* 
app has configured default export values (like psu-cashnet, for instance). 
The settings for these apps can be overridden in `settings.py` as `PSU_*_EXPORT_MODELS` (described below)

### The EXPORT_MODELS Settings
Each app can have its own EXPORT_MODELS setting prepended with the app's name. 
For example, psu-base would use `PSU_BASE_EXPORT_MODELS` and psu-cashnet would use `PSU_CASHNET_EXPORT_MODELS`. 

The app that you are deploying (call it Demo for example), can name the setting 
`DEMO_EXPORT_MODELS` or simply name it `EXPORT_MODELS`.

The `*EXPORT_MODELS` setting can be defined various ways:
1. `True`: Export all models in this app
1. `False`: Do not export any models from this app
1. `None`: 
   * In the case of an installed plugin/app, no models will be imported
   * In the case of a deployed app, all models will be imported by default
1. `['student', 'registration']`: Only the student and registration models will be exported
1. `['!student', '!registration']`: All models EXCEPT student and registration will be exported  

**Note about mixed inclusion/exclusion lists:**  
By putting an exclusion (!) in the list, you signify you want to include all models except those 
specifically excluded.  It does not make sense to also list models to include.  For this reason,
the existence of any exclusion (!) will cause all non-excluded models to be exported, regardless of 
their existence in the list.

## View Export Settings/Status
A view is included in the admin menu for Super-Users to view a list of all the models in the app 
(and installed apps) and whether they will be exported or not.  

There is also a button to manually run the export on the status page.