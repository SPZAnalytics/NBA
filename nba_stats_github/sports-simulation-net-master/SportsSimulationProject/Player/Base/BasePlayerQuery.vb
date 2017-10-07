Option Strict On

Imports System.Linq

Namespace Player
    Namespace Base
        Public Class BasePlayerQuery

            ''' <summary>
            ''' Singleton pattern - only need one BasePlayerQuery object.
            ''' </summary>
            Private Shared _Instance As BasePlayerQuery = Nothing
            
            ''' <summary>
            ''' Gets or creates instance of <see cref="BasePlayerQuery"/> object.
            ''' </summary>
            ''' <value>The instance.</value>
            Public Shared ReadOnly Property Instance() As BasePlayerQuery
                Get
                    If (_Instance Is Nothing) Then
                        _Instance = New BasePlayerQuery()
                    End If
                    Return _Instance
                End Get
            End Property

            ' ''' <summary>
            ' ''' Uses LINQ to query PlayerSeasons by single year.
            ' ''' </summary>
            ' ''' <param name="seasons">List of BasePlayerSeason objects.</param>
            ' ''' <param name="year1">The starting year.</param>
            ' ''' <param name="year2">The ending year.</param>
            ' ''' <returns>BasePlayerSeason object.</returns>
            Public Function QuerySeason(ByVal seasons As List(Of BasePlayerSeason), ByVal year As Integer) As BasePlayerSeason
                Dim result As New BasePlayerSeason
                Dim query = (From s As BasePlayerSeason In seasons
                            Where s.Year = year
                            Select s).First
                Return query
            End Function

            ' ''' <summary>
            ' ''' Uses LINQ to query PlayerSeasons by date range.
            ' ''' </summary>
            ' ''' <param name="seasons">List of BasePlayerSeason object.</param>
            ' ''' <param name="year1">The starting year.</param>
            ' ''' <param name="year2">The ending year.</param>
            ' ''' <returns>List of BasePlayerSeason objects.</returns>
            Public Function QuerySeasons(ByVal s As List(Of BasePlayerSeason), ByVal year1 As Integer, ByVal year2 As Integer) As List(Of BasePlayerSeason)
                If year1 > year2 Then
                    Throw New Exception("year1 parameter cannot be greater than year2 parameter")
                End If
                If s.Count < 1 Then
                    Throw New Exception("cannot query empty list of seasons")
                End If
                Dim results As New List(Of BasePlayerSeason)
                Dim query = From bps As BasePlayerSeason In s
                                Where bps.Year >= year1 And bps.Year <= year2
                                Select bps
                For Each bps As BasePlayerSeason In query
                    results.Add(bps)
                Next
                Return results
            End Function

            ' private methods
            ''' <summary>
            ''' Initializes a new instance of the <see cref="BasePlayerQuery" /> class.
            ''' </summary>
            ''' <remarks>Uses singleton pattern, so New is private.</remarks>
            Private Sub New()

            End Sub

        End Class
    End Namespace
End Namespace