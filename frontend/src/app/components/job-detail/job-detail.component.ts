import { Component, OnInit } from '@angular/core';

import { ActivatedRoute } from '@angular/router';
import { JobService } from 'src/app/services/job.service';
import { FormControl } from '@angular/forms';

// Interface
import { JobHeader } from 'src/app/interfaces/job_info';

// Service
import { BackToPlotlyService } from 'src/app/services/back-to-plotly.service';
@Component({
  selector: 'app-job-detail',
  templateUrl: './job-detail.component.html',
  styleUrls: ['./job-detail.component.css']
})
export class JobDetailComponent {
  job_header: JobHeader | undefined;
  // show_plot_1D: boolean;
  show_pReq_form: boolean;
  preProcess_CMDs: [];
  constructor(
    private route: ActivatedRoute,
    private jobService: JobService,
    // private location: Location
    private b2p:BackToPlotlyService
  ) {
    this.show_pReq_form = false;
    this.preProcess_CMDs = [];
  }

  ngOnInit(): void {
    this.getSample();
    this.show_pReq_form = false;
  }

  getSample(): void {
    const jobid = this.route.snapshot.paramMap.get('jobId');
    console.log('goes into job',jobid)
    if (jobid!= null){
      this.jobService.getJobDetail(jobid).subscribe(job_header => {
        this.job_header = job_header;
        console.log('return',this.job_header);
        console.log('return',this.job_header.axes);
        // for (const key of Object.keys(job_header.configs)) { 
        //   console.log(key + ": "); 
        //   console.log(job_header.configs[key]);
        // };
        });
    }
  }

  previewData(): void{
    console.log('press button previewData')
    
    this.show_pReq_form = !this.show_pReq_form;

  };

  get_preProcessCMDs(json_array: any) {
    console.log("get CMDs");
    this.preProcess_CMDs = json_array;
    console.log(this.preProcess_CMDs);
    }
  
  download_rawdata(){
    const jobid = this.route.snapshot.paramMap.get('jobId');
    if (jobid!= null){
      this.jobService.downloadJobRawdata(jobid).subscribe((res) => {
        let filename = res.headers.get('content-disposition').split('"')[1]
        console.log("download file", filename);
        let blob: Blob = new Blob([res.body]); // , { type: "application/pdf" });
        let downloadUrl = window.URL.createObjectURL(blob);
        let link = document.createElement("a");
        link.href = downloadUrl;
        link.download = filename;
        link.click();
      });
    }
    
  }
}
