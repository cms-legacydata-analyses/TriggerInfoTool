# How to know if the Trigger was accepted
## Usage Instruction

First you have to create a [VM](http://opendata.cern.ch/VM/CMS "CMS Open Data Portal") from the CMS Open Data website. 

Then follow these steps:

- Create a CMSSW environment: 

    ```
    cmsrel CMSSW_5_3_32
    ```

- Change to the CMSSW_5_3_32/src/ directory:

    ```
    cd CMSSW_5_3_32/src/
    ```

- Initialize the CMSSW environment:

  ```
  cmsenv
  ```

- Obtain the code from git and move it to the `src` area:

  ```
  git clone git://github.com/cms-legacydata-analyses/TriggerInfoTool.git
  cd TriggerInfoTool
  ```
  

- Go to the TriggerInfoTool/TriggerPrescalesAnalyzer area.  Note that the code lives under `src`

  ```
  cd TriggerPrescalesAnalyzer
  ```

- Compile everything:

  ```
  scram b
  ```

- Make a soft link to the python configuration file

```
ln -s python/prescalesinfoanalyzer_cfg.py .
```

- Make symbolic links to the conditions database

```
ln -sf /cvmfs/cms-opendata-conddb.cern.ch/FT_53_LV5_AN1_RUNA FT_53_LV5_AN1
ln -sf /cvmfs/cms-opendata-conddb.cern.ch/FT_53_LV5_AN1_RUNA.db FT_53_LV5_AN1_RUNA.db
```

- Make sure the `cms-opendata-conddb.cern.ch` directory has actually expanded in your VM.  One way of doing this is executing:

```
ls -l
ls -l /cvmfs/
```

You should now see the `cms-opendata-conddb.cern.ch` link in the `/cvmfs` area.


- Run the CMSSW executable in the background

```
cmsRun prescalesinfoanalyzer_cfg.py > full.log 2>&1 &
```

- Check the development of the job:

```
tailf full.log
```

*NOTE*: The first time you execute the job, it will take a long time (depending on your connection speed) to the point that it looks like it is not doing anything.  That is fine.  This is because the database payload files will be downloaded/cached locally in the VM.  Later attempts should be faster, however.
