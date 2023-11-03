import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { AnaRequest_resonator, PlotRequestTypes2Label } from 'src/app/interfaces/data_extract'
import { ActivatedRoute } from '@angular/router';
import { Validators } from '@angular/forms';

import { AnalysisService } from 'src/app/services/analysis.service';

import { JobService } from 'src/app/services/job.service';
import { BackToPlotlyService } from 'src/app/services/back-to-plotly.service';
@Component({
  selector: 'app-single-shot-distribution',
  templateUrl: './single-shot-distribution.component.html',
  styleUrls: ['./single-shot-distribution.component.css']
})
export class SingleShotDistributionComponent {
  ana_ReqForm = this.fb.group({
    prePro_req: ['[]',Validators.required],
    ana_req: ['{}',Validators.required],
  });
  graph: any;
  imageSrc: any;
  show_plot: boolean ;
  constructor(  private fb:FormBuilder,
    private route: ActivatedRoute,
    private jobService: JobService,
    private analysisService: AnalysisService,
    // private location: Location
    private b2p:BackToPlotlyService ) {
      this.show_plot = false;
    }
  do_analysis(){

      console.log("Analysis")
      let jsonObj_preProcess = JSON.parse(this.ana_ReqForm.value.prePro_req!);
      let jsonObj_ana = JSON.parse(this.ana_ReqForm.value.ana_req!);
      console.log(jsonObj_preProcess,jsonObj_ana)
      this.analysisService.getTrainingData(jsonObj_preProcess,jsonObj_ana).subscribe(blob => {
          const url = URL.createObjectURL(blob);
          this.imageSrc = url;
          this.show_plot = true;
        });

      
    
  }

  download(){

    this.analysisService.downloadAnalysisResult().subscribe((res) => {
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
