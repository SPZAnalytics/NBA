Option Strict On

Namespace Player
    Namespace Base
        Public Class BasePlayer

            ''' <summary>
            ''' Gets or sets the birth date.
            ''' </summary>
            ''' <value>The birth date.</value>
            Public Property BirthDate() As Date
            ''' <summary>
            ''' Gets or sets the first name.
            ''' </summary>
            ''' <value>The first name.</value>
            Public Property FirstName() As String
            ''' <summary>
            ''' Gets or sets the height.
            ''' </summary>
            ''' <value>The height (inches).</value>
            Public Property Height() As Integer
            ''' <summary>
            ''' Gets or sets the ids.
            ''' </summary>
            ''' <value>List of <see cref="BasePlayerId"></see> objects.</value>
            Public Property Ids() As List(Of BasePlayerId) = New List(Of BasePlayerId)
            ''' <summary>
            ''' Gets or sets the last name.
            ''' </summary>
            ''' <value>The last name.</value>
            Public Property LastName() As String
            ''' <summary>
            ''' Gets or sets the name of the middle.
            ''' </summary>
            ''' <value>The name of the middle.</value>
            Public Property MiddleName() As String
            ''' <summary>
            ''' Gets or instantiates query object.
            ''' </summary>
            ''' <value><see cref="BasePlayerQuery"></see> object.</value>
            Public Property Query As BasePlayerQuery
            ''' <summary>
            ''' Gets or sets list of seasons.
            ''' </summary>
            ''' <value>List of <see cref="BasePlayerSeason"></see> objects.</value>
            Public Property Seasons() As List(Of BasePlayerSeason) = New List(Of BasePlayerSeason)
            ''' <summary>
            ''' Gets or sets the suffix (jr., III, etc.)
            ''' </summary>
            ''' <value>The suffix.</value>
            Public Property Suffix() As String
            ''' <summary>
            ''' Gets or sets the weight.
            ''' </summary>
            ''' <value>The weight (pounds).</value>
            Public Property Weight() As Integer

            ''' <summary>
            ''' Initializes a new instance of the <see cref="BasePlayer" /> class.
            ''' </summary>
            Public Sub New()
                Me.Query = BasePlayerQuery.Instance
            End Sub

            ''' <summary>
            ''' Adds <see cref="BasePlayerId"></see> object.
            ''' </summary>
            ''' <param name="id"><see cref="BasePlayerId"></see></param>
            Public Sub AddId(ByVal id As BasePlayerId)
                Me.Ids.Add(id)
            End Sub

            ''' <summary>
            ''' Adds List of <see cref="BasePlayerId"></see> object to existing list.
            ''' </summary>
            ''' <param name="ids">List of <see cref="BasePlayerId"></see>.</param>
            Public Sub AddIds(ByVal ids As List(Of BasePlayerId))
                For Each id As BasePlayerId In ids
                    Me.AddId(id)
                Next
            End Sub

            ''' <summary>
            ''' Adds <see cref="BasePlayerSeason"></see> to list of seasons.
            ''' </summary>
            ''' <param name="season"><see cref="BasePlayerSeason"></see></param>
            Public Sub AddSeason(ByVal season As BasePlayerSeason)
                Me.Seasons.Add(season)
            End Sub

            ''' <summary>
            ''' Adds List of <see cref="BasePlayerSeason"></see> object to existing list.
            ''' </summary>
            ''' <param name="seasons">List of <see cref="BasePlayerSeason"></see>.</param>
            Public Sub AddSeasons(ByVal seasons As List(Of BasePlayerSeason))
                For Each season As BasePlayerSeason In seasons
                    Me.AddSeason(season)
                Next
            End Sub

            ''' <summary>
            ''' Calculates total over all seasons in Seasons property.
            ''' </summary>
            ''' <param name="statname">The name of the statistic to calculate the total.</param>
            ''' <returns>Total of a single statistic.</returns>
            Public Function CareerTotal(ByVal statname As String) As Double
                Dim tot As Double = 0
                For Each s As BasePlayerSeason In Me.Seasons
                    Dim stot As Double = s.GetSeasonTotal(statname)
                    tot += stot
                Next
                Return tot
            End Function

            ''' <summary>
            ''' Gets the base player ids.
            ''' </summary>
            ''' <returns>List of ids</returns>
            Public Function GetBasePlayerIds() As List(Of BasePlayerId)
                Return Me.Ids
            End Function

            ''' <summary>
            ''' Gets all <see cref="BasePlayerSeason"></see> in list.
            ''' </summary>
            ''' <returns><see cref="BasePlayerSeason"></see></returns>
            Public Function GetCareer() As List(Of BasePlayerSeason)
                Return Me.Seasons
            End Function

            ''' <summary>
            ''' Gets list of id strings.
            ''' </summary>
            ''' <returns>List of String</returns>
            Public Function GetIdStrings() As List(Of String)
                Dim ids As New List(Of String)
                For Each id In Me.Ids
                    ids.Add(id.Id)
                Next
                Return ids
            End Function

            ''' <summary>
            ''' Gets dictionary of the ids and sources.
            ''' </summary>
            ''' <returns>Dictionary of String, String</returns>
            Public Function GetIdsAndSources() As Dictionary(Of String, String)
                Dim hash As New Dictionary(Of String, String)
                For Each id In Me.Ids
                    hash.Add(id.Id, id.Source)
                Next
                Return hash
            End Function

            ''' <summary>
            ''' Gets single season from List of seasons.
            ''' </summary>
            ''' <param name="year">The season year.</param>
            ''' <returns><see cref="BasePlayerSeason"></see></returns>
            Public Function GetSeason(ByVal year As Integer) As BasePlayerSeason
                Dim gottenSeason As BasePlayerSeason = Me.Query.QuerySeason(Me.Seasons, year)
                Return gottenSeason
            End Function

            ''' <summary>
            ''' Gets single PlayerSeason object from Seasons list.
            ''' </summary>
            ''' <param name="year">The season year.</param>
            ''' <returns>A single PlayerSeason object.</returns>
            Public Function GetSeason(ByVal seasons As List(Of BasePlayerSeason), ByVal year As Integer) As BasePlayerSeason
                Dim gottenSeason As BasePlayerSeason = Me.Query.QuerySeason(seasons, year)
                Return gottenSeason
            End Function

            ''' <summary>
            ''' Gets list of seasons based on date range.
            ''' </summary>
            ''' <param name="year1">Starting year.</param>
            ''' <param name="year2">Ending year.</param>
            ''' <returns>List of <see cref="BasePlayerSeason"></see></returns>
            Public Function GetSeasons(ByVal year1 As Integer, ByVal year2 As Integer) As List(Of BasePlayerSeason)
                Dim gottenSeasons As List(Of BasePlayerSeason) = Me.Query.QuerySeasons(Me.Seasons, year1, year2)
                Return gottenSeasons
            End Function

            ''' <summary>
            ''' Gets a list seasons based on date range.
            ''' </summary>
            ''' <param name="lbps">List of <see cref="BasePlayerSeason"></see></param>
            ''' <param name="year1">Starting year.</param>
            ''' <param name="year2">Ending year.</param>
            ''' <returns>List of <see cref="BasePlayerSeason"></see></returns>
            Public Function GetSeasons(ByVal lbps As List(Of BasePlayerSeason), ByVal year1 As Integer, ByVal year2 As Integer) As List(Of BasePlayerSeason)
                Me.Query = BasePlayerQuery.Instance
                Dim gottenSeasons As List(Of BasePlayerSeason) = Me.Query.QuerySeasons(lbps, year1, year2)
                Return gottenSeasons
            End Function

            ''' <summary>
            ''' Gets the season total for a particular statistic.
            ''' </summary>
            ''' <param name="statName">Statistic name.</param>
            ''' <param name="year">The season year.</param>
            ''' <returns>Double</returns>
            Public Function GetSeasonTotal(ByVal statName As String, ByVal year As Integer) As Double
                Dim tot As Double = 0
                Dim s As BasePlayerSeason = Me.GetSeason(year)
                tot = s.GetSeasonTotal(statName)
                Return tot
            End Function

            ''' <summary>
            ''' Gets a List of String of the sources for id values.
            ''' </summary>
            ''' <returns>List of String</returns>
            Public Function GetSources() As List(Of String)
                Dim sources As New List(Of String)
                For Each id In Me.Ids
                    sources.Add(id.Source)
                Next
                Return sources
            End Function

            ''' <summary>
            ''' Returns the last season in a player's career.
            ''' </summary>
            ''' <returns><see cref="BasePlayerSeason"></see></returns>
            Public Function LastSeason() As BasePlayerSeason
                Dim max As Integer = Me.Seasons.Count - 1
                Return Me.Seasons(max)
            End Function

            Public Function MatchIdAndSource(ByVal players As List(Of BasePlayer), ByVal idToMatch As String, ByVal sourceToMatch As String) As BasePlayer
                Dim player As New BasePlayer
                For Each bp As BasePlayer In players
                    For Each id As BasePlayerId In Ids
                        If id.Id = idToMatch And id.Source = sourceToMatch Then
                            Return bp
                        End If
                    Next
                Next
                Return player
            End Function

            ''' <summary>
            ''' Returns total for statistic over a range of seasons.
            ''' </summary>
            ''' <param name="statname">The statname.</param>
            ''' <param name="startyear">The startyear.</param>
            ''' <param name="endyear">The endyear.</param>
            ''' <returns>Double</returns>
            Public Function SeasonRangeTotal(ByVal statname As String, ByVal startyear As Integer, ByVal endyear As Integer) As Double
                If Me.Seasons.Count < 1 Then
                    Throw New Exception("list of BasePlayerSeason cannot be empty")
                End If
                Dim tot As Double = 0
                Dim lbps As List(Of BasePlayerSeason) = Me.Query.QuerySeasons(Me.Seasons, startyear, endyear)
                For Each bps As BasePlayerSeason In lbps
                    Dim stot As Double = bps.GetSeasonTotal(statname)
                    tot += stot
                Next
                Return tot
            End Function

            ''' <summary>
            ''' Returns total for statistic over a range of seasons.
            ''' </summary>
            ''' <param name="s">List of <see cref="BasePlayerSeason"></see></param>
            ''' <param name="statname">The statname.</param>
            ''' <param name="startyear">The startyear.</param>
            ''' <param name="endyear">The endyear.</param>
            ''' <returns>Double</returns>
            Public Function SeasonRangeTotal(ByVal s As List(Of BasePlayerSeason), ByVal statname As String, ByVal startyear As Integer, ByVal endyear As Integer) As Double
                If s.Count < 1 Then
                    Throw New Exception("list of BasePlayerSeason cannot be empty")
                End If
                Dim tot As Double = 0
                Dim lbps As List(Of BasePlayerSeason) = Me.Query.QuerySeasons(s, startyear, endyear)
                For Each bps As BasePlayerSeason In lbps
                    Dim stot As Double = bps.GetSeasonTotal(statname)
                    tot += stot
                Next
                Return tot
            End Function

        End Class
    End Namespace
End Namespace