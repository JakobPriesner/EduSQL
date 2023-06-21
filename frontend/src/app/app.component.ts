import {Component, OnInit} from '@angular/core';
import {CookieService} from "../lib/services/cookie.service";
import {MatDialog} from "@angular/material/dialog";
import {ErmDialogComponent} from "./erm-dialog/erm-dialog.component";
import {InboxDialogComponent} from "./inbox-dialog/inbox-dialog.component";
import {InboxService} from "../lib/services/api/inbox.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  title = 'SQL';
  newMessageCount: number = this.inboxService.newMessageCount;

  constructor(public cookieService: CookieService,
              public dialog: MatDialog,
              public inboxService: InboxService) {
  }

  ngOnInit(): void {
    this.inboxService.newMessageCountSubject.subscribe(result => this.newMessageCount = result);
  }

  openErmDialog(): void {
    this.dialog.open(ErmDialogComponent);
  }

  openInboxDialog(): void {
    this.inboxService.clearSelection();
    const dialogRef = this.dialog.open(InboxDialogComponent, {
      width: '600px',
      height: '400px',
    });

    dialogRef.afterClosed().subscribe(() => {
      // Handle any necessary logic after the dialog is closed
    });
  }

}
