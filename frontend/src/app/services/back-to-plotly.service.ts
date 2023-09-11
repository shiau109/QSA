import { Injectable } from '@angular/core';
import * as PlotlyJS from 'plotly.js-dist-min';

@Injectable({
  providedIn: 'root'
})
export class BackToPlotlyService {

  constructor() { }

  data1DtTraces_dict( dict:any, x:string ){
    console.log(Object.keys(dict));
    let tr_names = Object.keys(dict)
    let traces = tr_names.map( (data_label,i) => {
      let trace = {
        x: dict[x],    
        y: dict[data_label],   
        mode:"markers",
        name: data_label,
        // type: "scatter",  
      };
      return trace;
    });
    return traces
  }
  data1DTraces(tr_names: string[], x:number[][], y:number[][]){
    let traces = {}
    if ( x.length == 1 ){
      traces = this.dataShareX(tr_names, x[0], y)
    }else{
      traces = this.dataXYTraces(tr_names, x, y)
    }
    return traces
  }
  dataShareX( tr_names: string[], x:number[], y:number[][]){ 
    let traces = tr_names.map( (data_label,i) => {
      let trace = {
        x: x,    
        y: y[i],   
        mode:"markers",
        name: data_label,
        // type: "scatter",  
      };
      return trace;
    });
    return traces;
  };
  dataXYTraces( tr_names: string[], x:number[][], y:number[][]){ 
    let traces = tr_names.map( (data_label,i) => {
      let trace = {
        x: x[i],    
        y: y[i],   
        mode:"markers",
        name: data_label,
        // type: "scatter",  
      };
      return trace;
     });
    return traces
  }

  dataContour( tr_names:string[], x:number[], y:number[], z:number[][]){
    let traces = tr_names.map( (data_label,i) => {
      let trace = {
        x: x,    
        y: y,  
        z: z[i], 
        type: 'heatmap',
        name: data_label,
        // type: "scatter",  
      };
      return trace;
     });
    return traces
  }

  plotLine(title: string, plotDiv: string, x:number[], y:number[]){           
    let trace = {
      x: x,    
      y: y,   
      mode:"markers",
      // type: "scatter",  
    };
                  
    let layout = {
      title:title
    };
    PlotlyJS.newPlot(plotDiv, [trace], layout);     
  };

  plotShareX(title: string, plotDiv: string, labels: string[], x:number[], y:number[]){ 
    let traces = labels.map( (l, i) => {
      let trace = {
        x: x,    
        y: y[i],   
        mode:"markers",
        name: l,
        // type: "scatter",  
      };
      return trace;
    });         

                  
    let layout = {
      title:title
    };
    PlotlyJS.newPlot(plotDiv, traces, layout);     
  }  
}
