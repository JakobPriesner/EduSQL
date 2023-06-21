import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-select-all-result-table',
  templateUrl: './select-all-result-table.component.html',
  styleUrls: ['./select-all-result-table.component.css']
})
export class SelectAllResultTableComponent implements OnInit {
  @Input() sqlResult: any;
  dataSource: { [key: string]: any }[] = [];
  displayedColumns: string[] = [];

  constructor() {

  }

  ngOnInit(): void {
    if (typeof this.sqlResult === "object") {
      this.dataSource = this.sqlResult ?? [];
      if (this.dataSource[0]){
        this.displayedColumns = Object.keys(this.dataSource[0]);
      }
    } else {
      this.dataSource = [];
    }
  }

}
