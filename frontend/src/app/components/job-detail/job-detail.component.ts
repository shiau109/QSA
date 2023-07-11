import { Component, OnInit } from '@angular/core';

import { Observable, Subject } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { JobService } from 'src/app/services/job.service';

import {
   debounceTime, distinctUntilChanged, switchMap
 } from 'rxjs/operators';
 import { JobHeader } from 'src/app/interfaces/job_header';
@Component({
  selector: 'app-job-detail',
  templateUrl: './job-detail.component.html',
  styleUrls: ['./job-detail.component.css']
})
export class JobDetailComponent {
  job_header: JobHeader | undefined;
  constructor(
    private route: ActivatedRoute,
    private jobService: JobService,
    // private location: Location
  ) {  }

  ngOnInit(): void {
    this.getSample();
  }

  getSample(): void {
    const sn = this.route.snapshot.paramMap.get('jobId');
    console.log('goes into job',sn)
    if (sn!= null){
      this.jobService.getJobDetail(sn).subscribe(job_header => {
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
  
  preview1D(): void{
    console.log('press button')
  }
}
