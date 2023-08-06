# gtimelog2toggl

This is a simple script for importing your [gtimelog](https://gtimelog.org/) into [Toggl Track](https://www.toggl.com/track/).


## Install

1. Install gtimelog2toggl using pip.

    ```
    pip install gtimelog2toggl
    ```

2. Update the configuration file by running gtimelog2toggl with the `-c` flag.

    ```
    gtimelog2toggl -c
    ```
   
    - One required field to make gtimelog2toggl work is the `api_key` which can be found in your Toggl profile [settings](https://support.toggl.com/en/articles/3116844-where-is-my-api-token-located).
    
    - You may also want to add mappings from a gtimelog category to a client and project found in Toggl. (NOTE: The client/project pair must already exist within Toggl) Any categories not mapped or entries without a category will be added to Toggl without any client/project attached.

    ```yaml
    api_key: <ADD API KEY HERE>
    
    mappings:
      acme: [ACME, General]
      acme_recruit: [ACME, Recruiting]
      acme_hr: [ACME, HR]
      llama: [LlamaCorp, General]
    ```


## Usage

Run `gtimelog2toggl` to automatically import your gtimelog entries to Toggl for the current week and then end of your work week.

```
gtimelog2toggl
```

More options may come in the future, but this works for me for now.

**WARNING**: There are currently no checks if a time entry has already been added. 
Duplicate entries will be added if you run this script more than once in the week.
I recommend you use the `--dry-run` argument beforehand to ensure everything is setup
correctly.
*(I may fix this in the future, if I have the motivation.)*
