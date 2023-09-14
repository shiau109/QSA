import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { AnaRequest_resonator, PlotRequestTypes2Label } from 'src/app/interfaces/data_extract'
import { ActivatedRoute } from '@angular/router';
import { Validators } from '@angular/forms';

import { AnalysisService } from 'src/app/services/analysis.service';

import { JobService } from 'src/app/services/job.service';
import { BackToPlotlyService } from 'src/app/services/back-to-plotly.service';
@Component({
  selector: 'app-resonator-analysis',
  templateUrl: './resonator-analysis.component.html',
  styleUrls: ['./resonator-analysis.component.css']
})
export class ResonatorAnalysisComponent {
  ana_ReqForm = this.fb.group({
    prePro_req: ['[]',Validators.required],
    ana_req: ['{}',Validators.required],
  });
  graph: any;
  constructor(  private fb:FormBuilder,
    private route: ActivatedRoute,
    private jobService: JobService,
    private analysisService: AnalysisService,
    // private location: Location
    private b2p:BackToPlotlyService ) {
    }
  
  do_analysis(){

      console.log("Analysis")
      let jsonObj_preProcess = JSON.parse(this.ana_ReqForm.value.prePro_req!);
      let jsonObj_ana = JSON.parse(this.ana_ReqForm.value.ana_req!);
      console.log(jsonObj_preProcess,jsonObj_ana)
      this.analysisService.get_resonator_qfactor(jsonObj_preProcess,jsonObj_ana).subscribe( data => {
      console.log('return',data);
      console.log(Object.keys(data));
      let fit_result_traces = this.b2p.data1DtTraces_dict(data,"index");
      this.graph = {
        data: fit_result_traces,
        layout: {width: 320, height: 240, title: 'Fit result'}
      };
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
