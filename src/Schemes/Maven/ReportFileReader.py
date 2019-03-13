from __future__ import annotations

from Schemes.Dependencies import Dependencies
from Exceptions.ParseFailureException import ParseFailureException


class ReportFileReader:
    report_file_path: str

    def __init__(self, reportFile: str):
        self.report_file_path = reportFile

    def read(self) -> Dependencies:
        result: Dependencies = Dependencies()

        try:
            with open(self.report_file_path) as report:
                for line in report:
                    parts = line.split(':')
                    if len(parts) >= 3:
                        result.append(parts[0] + ':' + parts[1], parts[2])
                    else:
                        raise ParseFailureException('failed parsing report line :' + line)

            report.closed
        except FileNotFoundError:
            print('WARN :: no report file : ' + self.report_file_path)
            pass

        return result
