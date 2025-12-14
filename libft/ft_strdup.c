/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/12 17:42:31 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/12 17:43:00 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stdio.h>
#include "libft.h"
#include <stdlib.h>

char	*ft_strdup(const char *s)
{
	int		len;
	char	*dest;

	len = ft_strlen(s) + 1;
	dest = (char *)malloc(len * sizeof(char));
	if (!dest)
		return (NULL);
	ft_memcpy(dest, s, len);
	return (dest);
}
