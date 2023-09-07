import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { PlotRequestTypesEnum, PlotRequestTypes2Label } from 'src/app/interfaces/data_extract'
import { ActivatedRoute } from '@angular/router';
import { Validators } from '@angular/forms';
import { Plot1DFuncRequest, ExpDataAxes, PlotContourRequest, PlotParEqRequest } from 'src/app/interfaces/data_extract'

import { JobService } from 'src/app/services/job.service';
import { BackToPlotlyService } from 'src/app/services/back-to-plotly.service';
@Component({
  selector: 'app-resonator-analysis',
  templateUrl: './resonator-analysis.component.html',
  styleUrls: ['./resonator-analysis.component.css']
})
export class ResonatorAnalysisComponent {
  analysisReqForm = this.fb.group({
    prePro_req: ['',Validators.required],
    ana_req: ['',Validators.required],
  });
  constructor(  private fb:FormBuilder,
    private route: ActivatedRoute,
    private jobService: JobService,
    // private location: Location
    private b2p:BackToPlotlyService ) {
    }
  
  do_analysis(){
      console.log("Analysis")
  }
}
