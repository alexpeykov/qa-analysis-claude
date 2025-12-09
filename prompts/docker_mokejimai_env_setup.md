# Mokejimai Application Setup

This prompt is used to set up and rebuild the Mokejimai application running in the `mokejimai` Docker container on the `ubuntu-remote` server.

## Prerequisites - USER INPUT REQUIRED

**⚠️ BEFORE USING THIS PROMPT: Replace `<BRANCH_NAME>` with your actual branch name**

---

## Complete Setup Command

```
In the mokejimai container on ubuntu-remote, run these commands sequentially in the /home/app/src directory:

1. git checkout <BRANCH_NAME>  ⚠️ REPLACE <BRANCH_NAME> WITH YOUR ACTUAL BRANCH
2. composer install
3. app/console maba:webpack:compile

Wait for each command to complete successfully before running the next one.
```

## What Each Command Does

1. **git checkout <BRANCH_NAME>**: Switches to the specified Git branch (e.g., CORE-5663 for a specific ticket)
2. **composer install**: Installs PHP dependencies from composer.json
3. **app/console maba:webpack:compile**: Compiles JavaScript/CSS assets using webpack
4. **app/console cache:clear**: Clears the Symfony application cache
5. **app/console maba:webpack:compile** (second run): Recompiles assets after cache clear to ensure everything is fresh

## Technical Details

- **Container**: mokejimai
- **Remote Server**: ubuntu-remote
- **Working Directory**: /home/app/src
- **Execution Method**: SSH to ubuntu-remote, then docker exec into mokejimai container
- **Expected Duration**: ~2-3 minutes total

## Notes

- Some deprecation warnings from Composer are expected (legacy packages)
- Webpack will show warnings about bundle sizes - these are normal
- All commands must complete without errors for the setup to be successful
