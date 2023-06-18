import { Component } from '@angular/core';
import {ChildrenOutletContexts} from "@angular/router";
import {CookieService} from "../lib/services/cookie.service";
import {MatDialog} from "@angular/material/dialog";
import {ErmDialogComponent} from "./erm-dialog/erm-dialog.component";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'SQL';

  constructor(private contexts: ChildrenOutletContexts,
              public cookieService: CookieService,
              public dialog: MatDialog) {
  }

  openErmDialog(): void {
    this.dialog.open(ErmDialogComponent);
  }
}
