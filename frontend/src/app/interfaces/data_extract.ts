import { JsonPipe } from "@angular/common";

export interface ExpDataAxes {
  name: string;
  position: number;
}

export interface Plot1DFuncRequest {
  x: string;
  y: string[];
  other_position:ExpDataAxes[];
}

export interface PlotParEqRequest {
  x: string;
  y: string;
  parameter: string;
  other_position:ExpDataAxes[];
}

export interface PlotContourRequest {
  x: string;
  y: string;
  z: string[];
  other_position:ExpDataAxes[];
}

export enum PlotRequestTypesEnum {
  F1 = "1DFunc",
  PE = "ParEq",
  F2 = "2D",
}
export const PlotRequestTypes2Label: Record<PlotRequestTypesEnum, string> = {
  [PlotRequestTypesEnum.F1]: "1D function (var vs data)",
  [PlotRequestTypesEnum.PE]: "Parametric equation (data vs data)",
  [PlotRequestTypesEnum.F2]: "2D map",
};