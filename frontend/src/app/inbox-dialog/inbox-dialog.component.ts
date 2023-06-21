import { Component } from '@angular/core';
import {InboxService} from "../../lib/services/api/inbox.service";
import {Message} from "../../lib/models/message.interface";
import {MatDialogRef} from "@angular/material/dialog";
import {ErmDialogComponent} from "../erm-dialog/erm-dialog.component";

@Component({
  selector: 'app-inbox-dialog',
  templateUrl: './inbox-dialog.component.html',
  styleUrls: ['./inbox-dialog.component.scss']
})
export class InboxDialogComponent {
  messages: Message[] = [];

  constructor(private inboxService: InboxService,
              public dialogRef: MatDialogRef<ErmDialogComponent>) {
    this.messages = inboxService.getMessages();
  }

  selectMessage(index: number): void {

  }

  onNoClick(): void {
    this.dialogRef.close();
  }
}
